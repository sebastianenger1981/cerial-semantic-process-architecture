"""
Deterministic PDF & High-Resolution Plot PNG Exporter for the CSI Process Blueprint.
Uses Headless Chrome + Chrome DevTools Protocol (CDP) with subprocess.DEVNULL
and strict timeouts so child processes never block or hang.
Exports:
  1. ./csi-process-blueprint/CSI_Process_Blueprint.pdf
  2. ./csi-process-blueprint/assets/fig5_phase_space_z_boundary.png
  3. ./csi-process-blueprint/assets/fig6_automation_sovereignty_matrix.png
"""

import asyncio
import base64
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import websockets


ROOT_DIR = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT_DIR / "CSI_Process_Blueprint.html"
PDF_PATH = ROOT_DIR / "CSI_Process_Blueprint.pdf"
ASSETS_DIR = ROOT_DIR / "assets"

PLOT_TARGETS = [
    ("fig5_phase_space_z_boundary.svg", "fig5_phase_space_z_boundary.png"),
    ("fig6_automation_sovereignty_matrix.svg", "fig6_automation_sovereignty_matrix.png"),
]


def find_browser() -> str:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError("Neither Google Chrome nor Microsoft Edge was found.")


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def parse_svg_dimensions(svg_path: Path) -> tuple[int, int]:
    tree = ET.parse(svg_path)
    root = tree.getroot()
    view_box = root.attrib.get("viewBox", "")
    if view_box:
        parts = [float(x) for x in view_box.replace(",", " ").split()]
        if len(parts) == 4:
            return int(round(parts[2])), int(round(parts[3]))
    width = int(float(root.attrib.get("width", "1100").replace("px", "")))
    height = int(float(root.attrib.get("height", "680").replace("px", "")))
    return width, height


class CDPSession:
    def __init__(self, ws):
        self.ws = ws
        self.msg_id = 0

    async def call(self, method: str, params: dict | None = None, timeout: float = 20.0) -> dict:
        self.msg_id += 1
        target_id = self.msg_id
        payload = {"id": target_id, "method": method, "params": params or {}}
        await asyncio.wait_for(self.ws.send(json.dumps(payload)), timeout=timeout)
        deadline = time.monotonic() + timeout
        while True:
            rem = max(0.5, deadline - time.monotonic())
            raw = await asyncio.wait_for(self.ws.recv(), timeout=rem)
            data = json.loads(raw)
            if data.get("id") == target_id:
                if "error" in data:
                    raise RuntimeError(f"CDP error on {method}: {data['error']}")
                return data.get("result", {})

    async def navigate_and_settle(self, url: str, timeout: float = 15.0) -> None:
        self.msg_id += 1
        nav_id = self.msg_id
        await asyncio.wait_for(
            self.ws.send(
                json.dumps({"id": nav_id, "method": "Page.navigate", "params": {"url": url}})
            ),
            timeout=5.0,
        )
        nav_ack = False
        load_fired = False
        deadline = time.monotonic() + timeout
        while not (nav_ack and load_fired):
            rem = deadline - time.monotonic()
            if rem <= 0:
                break
            try:
                raw = await asyncio.wait_for(self.ws.recv(), timeout=min(1.0, rem))
                data = json.loads(raw)
                if data.get("id") == nav_id:
                    nav_ack = True
                if data.get("method") == "Page.loadEventFired":
                    load_fired = True
            except asyncio.TimeoutError:
                if nav_ack:
                    # Check document.readyState directly so cached/fast loads never miss event
                    res = await self.call(
                        "Runtime.evaluate",
                        {"expression": "document.readyState", "returnByValue": True},
                        timeout=3.0,
                    )
                    if res.get("result", {}).get("value") == "complete":
                        break


async def export_all(port: int) -> None:
    targets = None
    for _ in range(40):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=1.0) as resp:
                items = json.loads(resp.read().decode("utf-8"))
                pages = [item for item in items if item.get("type") == "page"]
                if pages:
                    targets = pages[0]
                    break
        except Exception:
            await asyncio.sleep(0.25)

    if not targets or "webSocketDebuggerUrl" not in targets:
        raise RuntimeError("Could not connect to headless browser CDP page target.")

    ws_url = targets["webSocketDebuggerUrl"]
    async with websockets.connect(
        ws_url, max_size=150 * 1024 * 1024, open_timeout=10.0, close_timeout=2.0
    ) as ws:
        cdp = CDPSession(ws)
        await cdp.call("Page.enable", timeout=5.0)
        await cdp.call("Runtime.enable", timeout=5.0)

        html_uri = HTML_PATH.resolve().as_uri()
        print(f"[1/3] Loading HTML Blueprint: {html_uri}", flush=True)
        await cdp.navigate_and_settle(html_uri, timeout=15.0)

        img_check = await cdp.call(
            "Runtime.evaluate",
            {
                "expression": """
                (async () => {
                    document.documentElement.setAttribute('data-theme', 'light');
                    const imgs = Array.from(document.images);
                    await Promise.race([
                        Promise.all(imgs.map(img => {
                            if (img.complete) return Promise.resolve();
                            return new Promise(res => { img.onload = res; img.onerror = res; });
                        })),
                        new Promise(res => setTimeout(res, 5000))
                    ]);
                    return imgs.map(i => ({
                        file: i.src.split('/').pop(),
                        ok: i.complete && i.naturalWidth > 0,
                        w: i.naturalWidth,
                        h: i.naturalHeight
                    }));
                })()
                """,
                "awaitPromise": True,
                "returnByValue": True,
            },
            timeout=10.0,
        )
        statuses = img_check.get("result", {}).get("value", [])
        print(f"      -> Verified {len(statuses)} embedded images: {statuses}", flush=True)

        await cdp.call(
            "Emulation.setDeviceMetricsOverride",
            {"width": 1203, "height": 714, "deviceScaleFactor": 1, "mobile": False},
            timeout=5.0,
        )
        vp_check = await cdp.call(
            "Runtime.evaluate",
            {
                "expression": "({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth})",
                "returnByValue": True,
            },
            timeout=5.0,
        )
        print(f"      -> Viewport 1203x714 layout check: {vp_check.get('result', {}).get('value')}", flush=True)
        await cdp.call("Emulation.clearDeviceMetricsOverride", timeout=5.0)
        await asyncio.sleep(0.2)

        print("[2/3] Rendering multi-page print-optimized PDF...", flush=True)
        pdf_res = await cdp.call(
            "Page.printToPDF",
            {
                "printBackground": True,
                "preferCSSPageSize": True,
                "displayHeaderFooter": False,
                "scale": 1.0,
            },
            timeout=25.0,
        )
        pdf_bytes = base64.b64decode(pdf_res["data"])
        PDF_PATH.write_bytes(pdf_bytes)
        print(f"      -> Wrote {PDF_PATH.name} ({len(pdf_bytes):,} bytes)", flush=True)

        print("[3/3] Exporting 2x high-DPI PNG mathematical plots...", flush=True)
        for svg_name, png_name in PLOT_TARGETS:
            svg_path = ASSETS_DIR / svg_name
            png_path = ASSETS_DIR / png_name
            w, h = parse_svg_dimensions(svg_path)
            await cdp.call(
                "Emulation.setDeviceMetricsOverride",
                {
                    "width": w,
                    "height": h,
                    "deviceScaleFactor": 2,
                    "mobile": False,
                },
                timeout=5.0,
            )
            await cdp.navigate_and_settle(svg_path.resolve().as_uri(), timeout=10.0)
            await asyncio.sleep(0.2)
            shot = await cdp.call(
                "Page.captureScreenshot",
                {
                    "format": "png",
                    "clip": {"x": 0, "y": 0, "width": w, "height": h, "scale": 1},
                },
                timeout=10.0,
            )
            png_bytes = base64.b64decode(shot["data"])
            png_path.write_bytes(png_bytes)
            print(f"      -> Wrote {png_path.name} ({len(png_bytes):,} bytes, {w*2}x{h*2}px)", flush=True)


def kill_process_tree(pid: int) -> None:
    subprocess.run(
        ["taskkill", "/F", "/T", "/PID", str(pid)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=5,
        check=False,
    )


def main() -> int:
    if not HTML_PATH.is_file():
        print(f"ERROR: Missing {HTML_PATH}", file=sys.stderr)
        return 1

    browser = find_browser()
    port = get_free_port()
    profile_dir = tempfile.mkdtemp(prefix="csi_pdf_cdp_")
    print(f"Using browser: {browser} (CDP port {port})", flush=True)

    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-networking",
        "--allow-file-access-from-files",
        f"--user-data-dir={profile_dir}",
        f"--remote-debugging-port={port}",
        "about:blank",
    ]

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    try:
        asyncio.run(asyncio.wait_for(export_all(port), timeout=50.0))
    finally:
        kill_process_tree(proc.pid)
        try:
            proc.wait(timeout=3)
        except Exception:
            pass
        shutil.rmtree(profile_dir, ignore_errors=True)

    if not PDF_PATH.is_file() or PDF_PATH.stat().st_size < 10_000:
        print("ERROR: PDF output missing or unexpectedly small!", file=sys.stderr)
        return 2

    print("SUCCESS: PDF handout and PNG plots verified on disk.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
