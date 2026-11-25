#!/usr/bin/env python3
"""
CSI Process Design Blueprint — Precision Vector & Numerical Plot Generator
Author: Antigravity Systems Architect (for Sebastian Enger, M.Sc. — Cypher Semantic Intelligence)

Generates Figures 1–6 in ./csi-process-blueprint/assets/:
  - fig1_architecture_stack.svg
  - fig2_master_workflow.svg
  - fig3_z_violation_gate.svg
  - fig4_fractal_dual_scale.svg
  - fig5_phase_space_z_boundary.svg
  - fig6_automation_sovereignty_matrix.svg

Validates every SVG via xml.etree.ElementTree to guarantee zero syntax errors.
"""

import math
import os
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

FONT_SANS = "'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif"
FONT_MONO = "'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace"


def esc(text: str) -> str:
    return escape(str(text), {'"': "&quot;", "'": "&apos;"})


def common_defs() -> str:
    return """
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#F1F5F9"/>
    </linearGradient>
    <linearGradient id="navyGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E3A8A"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#B45309"/>
      <stop offset="50%" stop-color="#D97706"/>
      <stop offset="100%" stop-color="#F59E0B"/>
    </linearGradient>
    <linearGradient id="emeraldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#065F46"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0369A1"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
    <linearGradient id="crimsonGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#991B1B"/>
      <stop offset="100%" stop-color="#DC2626"/>
    </linearGradient>
    <linearGradient id="spineGrad" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="50%" stop-color="#1E3A8A"/>
      <stop offset="100%" stop-color="#0284C7"/>
    </linearGradient>
    <filter id="cardShadow" x="-4%" y="-4%" width="108%" height="112%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
    <marker id="arrowSlate" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#334155"/>
    </marker>
    <marker id="arrowBlue" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#0284C7"/>
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#059669"/>
    </marker>
    <marker id="arrowAmber" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#D97706"/>
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#DC2626"/>
    </marker>
  </defs>
"""


def header_banner(width: int, fig_tag: str, title: str, subtitle: str) -> str:
    return f"""
  <rect x="0" y="0" width="{width}" height="82" fill="url(#navyGrad)"/>
  <rect x="0" y="79" width="{width}" height="3" fill="url(#goldGrad)"/>
  <text x="36" y="32" font-family="{FONT_MONO}" font-size="11.5" font-weight="700" fill="#FBBF24" letter-spacing="1.4">{esc(fig_tag)}</text>
  <text x="36" y="55" font-family="{FONT_SANS}" font-size="19.5" font-weight="800" fill="#FFFFFF">{esc(title)}</text>
  <text x="36" y="72" font-family="{FONT_SANS}" font-size="12" font-weight="400" fill="#CBD5E1">{esc(subtitle)}</text>
"""


def save_and_validate_svg(filename: str, svg_content: str) -> str:
    out_path = os.path.join(ASSETS_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip() + "\n")
    # Strict XML parse check
    ET.fromstring(svg_content.encode("utf-8"))
    size = os.path.getsize(out_path)
    print(f"[OK] {filename} ({size:,} bytes) — XML valid")
    return out_path


# ==============================================================================
# FIGURE 1: THE CSI PROCESS ARCHITECTURE STACK
# ==============================================================================
def build_fig1():
    W, H = 1200, 830
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        common_defs(),
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bgGrad)" rx="10"/>',
        header_banner(
            W,
            "FIGURE 1 • ARCHITECTURAL STACK",
            "The Cerial Semantic Process Architecture (CSPA / EPCSIS-P v2.0)",
            "Five-Layer Fractal Hierarchy Governed by PCSD Semantic Duality and the Non-Negotiable Z-Violation Invariant"
        ),
    ]

    # Left Vertical Z-Shield & Telemetry Bus
    parts.append(f"""
  <rect x="32" y="102" width="102" height="696" rx="10" fill="url(#spineGrad)" filter="url(#cardShadow)"/>
  <rect x="35" y="105" width="96" height="690" rx="8" fill="none" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="5,4"/>
  <text x="83" y="136" text-anchor="middle" font-family="{FONT_MONO}" font-size="11" font-weight="700" fill="#FBBF24">EPCSIS</text>
  <text x="83" y="153" text-anchor="middle" font-family="{FONT_MONO}" font-size="11" font-weight="700" fill="#FFFFFF">Z[N + 1]</text>
  <line x1="48" y1="166" x2="118" y2="166" stroke="#64748B" stroke-width="1"/>
  <g transform="translate(83, 445) rotate(-90)">
    <text x="0" y="-6" text-anchor="middle" font-family="{FONT_SANS}" font-size="13" font-weight="700" fill="#FFFFFF" letter-spacing="1.2">CONTINUOUS Z-SHIELD &amp; LIVE σ_Z TELEMETRY RAIL</text>
    <text x="0" y="13" text-anchor="middle" font-family="{FONT_MONO}" font-size="10.5" fill="#BAE6FD">Green ≤ 1.07  |  Amber ≤ 1.15 (CERIAL Ω)  |  Red &gt; 1.15 (Halt)</text>
  </g>
  <text x="83" y="768" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="#FDE68A">AXIOM 0</text>
  <text x="83" y="783" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" fill="#FFFFFF">LOCKED</text>
""")

    # Horizontal connectors from left spine to each layer
    for cy in [168, 322, 488, 622, 745]:
        parts.append(f'<line x1="134" y1="{cy}" x2="156" y2="{cy}" stroke="#D97706" stroke-width="2.2" marker-end="url(#arrowAmber)"/>')

    # LAYER 4: Dual-Scale Fractal Execution Layer (y=102..234)
    parts.append(f"""
  <rect x="158" y="102" width="1010" height="132" rx="10" fill="#FFFFFF" stroke="#0284C7" stroke-width="2" filter="url(#cardShadow)"/>
  <rect x="158" y="102" width="1010" height="32" rx="9" fill="#E0F2FE"/>
  <text x="176" y="123" font-family="{FONT_MONO}" font-size="11.5" font-weight="700" fill="#0369A1">LAYER 4 • FRACTAL EXECUTION SCALES (X — Operational Netnode Delivery)</text>
  <text x="1150" y="123" text-anchor="end" font-family="{FONT_MONO}" font-size="11" font-weight="600" fill="#0369A1">Same Core Grammar</text>

  <!-- Enterprise Card -->
  <rect x="176" y="144" width="476" height="78" rx="7" fill="#F8FAFC" stroke="#BAE6FD" stroke-width="1.5"/>
  <circle cx="196" cy="164" r="7" fill="#0284C7"/>
  <text x="211" y="168" font-family="{FONT_SANS}" font-size="13.5" font-weight="700" fill="#0F172A">Scale A: Enterprise &amp; Corporate Mode</text>
  <text x="192" y="189" font-family="{FONT_SANS}" font-size="11.5" fill="#334155">• Autonomous Delivery Squads, SRE/IT Ops &amp; CI/CD Change Gates</text>
  <text x="192" y="207" font-family="{FONT_SANS}" font-size="11.5" fill="#334155">• Cross-Department APIs, Customer Value Streams &amp; EU AI Act Audits</text>

  <!-- Isomorphism Bridge -->
  <text x="663" y="188" text-anchor="middle" font-family="{FONT_SANS}" font-size="18" font-weight="800" fill="#0284C7">↔</text>

  <!-- Daily Life Card -->
  <rect x="674" y="144" width="476" height="78" rx="7" fill="#F0FDF4" stroke="#A7F3D0" stroke-width="1.5"/>
  <circle cx="694" cy="164" r="7" fill="#059669"/>
  <text x="709" y="168" font-family="{FONT_SANS}" font-size="13.5" font-weight="700" fill="#0F172A">Scale B: Sovereign Daily Life Mode</text>
  <text x="690" y="189" font-family="{FONT_SANS}" font-size="11.5" fill="#334155">• M.E.A.T. Shield (Money, Energy, Attention, Time) &amp; Habit Loops</text>
  <text x="690" y="207" font-family="{FONT_SANS}" font-size="11.5" fill="#334155">• 5:30–22:15 Dual-Aspect Cadence, Solo Projects &amp; Clear Boundaries</text>
""")

    # LAYER 3: Four Functional Pillars (y=250..404)
    parts.append(f"""
  <rect x="158" y="250" width="1010" height="154" rx="10" fill="#FFFFFF" stroke="#1E3A8A" stroke-width="2" filter="url(#cardShadow)"/>
  <rect x="158" y="250" width="1010" height="32" rx="9" fill="#DBEAFE"/>
  <text x="176" y="271" font-family="{FONT_MONO}" font-size="11.5" font-weight="700" fill="#1E3A8A">LAYER 3 • FOUR FUNCTIONAL PILLARS (Y = N + 1 — Source Architecture &amp; Control)</text>
  <text x="1150" y="271" text-anchor="end" font-family="{FONT_MONO}" font-size="11" font-weight="600" fill="#1E3A8A">EPCSIS = Z[N+1]</text>
""")
    pillars = [
        ("1. Process Optimization", "#1E40AF", "#EFF6FF", [
            "PCSD x.n ~ y.m alignment",
            "Legacy decontamination",
            "Eliminate friction &amp; waste"
        ]),
        ("2. Process Automation", "#0369A1", "#F0F9FF", [
            "Bounded autonomy Z[N+1]",
            "HitL damping h &gt; h_crit",
            "AI Safety Z-Law guardrails"
        ]),
        ("3. Process Integration", "#047857", "#ECFDF5", [
            "Cypher Semantic Netnodes",
            "LCC / FCC / ACC protocols",
            "Strict Zero-DCC firewall"
        ]),
        ("4. Governance &amp; Telemetry", "#B45309", "#FFFBEB", [
            "3-Tier ϒ → Y → X roles",
            "4D Δ-Tolerance exception",
            "CCR: Check, Copy, Release"
        ]),
    ]
    px = 176
    for title_p, stroke_c, bg_c, bullets in pillars:
        parts.append(f"""
  <rect x="{px}" y="294" width="233" height="98" rx="7" fill="{bg_c}" stroke="{stroke_c}" stroke-width="1.4"/>
  <text x="{px + 12}" y="315" font-family="{FONT_SANS}" font-size="12.5" font-weight="800" fill="{stroke_c}">{title_p}</text>
  <text x="{px + 12}" y="337" font-family="{FONT_SANS}" font-size="11.2" fill="#1E293B">• {bullets[0]}</text>
  <text x="{px + 12}" y="356" font-family="{FONT_SANS}" font-size="11.2" fill="#1E293B">• {bullets[1]}</text>
  <text x="{px + 12}" y="375" font-family="{FONT_SANS}" font-size="11.2" fill="#1E293B">• {bullets[2]}</text>
""")
        px += 247

    # LAYER 2: Purified Classical DNA (y=420..556)
    parts.append(f"""
  <rect x="158" y="420" width="1010" height="136" rx="10" fill="#FFFFFF" stroke="#475569" stroke-width="1.8" filter="url(#cardShadow)"/>
  <rect x="158" y="420" width="1010" height="32" rx="9" fill="#E2E8F0"/>
  <text x="176" y="441" font-family="{FONT_MONO}" font-size="11.5" font-weight="700" fill="#1E293B">LAYER 2 • PURIFIED CLASSICAL DNA (x.n Syntactic Methods — Z-Audited, Zero Textbook Jargon)</text>
""")
    dna_cards = [
        ("Design Thinking DNA (Adaptive Front-End)", "#7C3AED", [
            "Resonant Need Sensing (LCC) → Intent Framing",
            "Rapid Netnode Prototyping &amp; Lived-Reality Testing"
        ]),
        ("PRINCE2 7th Ed. DNA (Controlled Execution)", "#0F766E", [
            "Continued Purpose &amp; Z Justification • Stage Gates",
            "Outcome-Product Planning • Management by Exception"
        ]),
        ("ITIL 4 DNA (Continuous Value &amp; Stability)", "#1D4ED8", [
            "End-to-End Value Streams • Swarm Incident Recovery",
            "Root Entropy Elimination • Shielded Change Flow"
        ]),
    ]
    dx = 176
    for dtitle, dcol, dlines in dna_cards:
        parts.append(f"""
  <rect x="{dx}" y="463" width="314" height="80" rx="7" fill="#F8FAFC" stroke="{dcol}" stroke-width="1.4"/>
  <text x="{dx + 14}" y="485" font-family="{FONT_SANS}" font-size="12.2" font-weight="700" fill="{dcol}">{dtitle}</text>
  <text x="{dx + 14}" y="507" font-family="{FONT_SANS}" font-size="11.2" fill="#334155">• {dlines[0]}</text>
  <text x="{dx + 14}" y="526" font-family="{FONT_SANS}" font-size="11.2" fill="#334155">• {dlines[1]}</text>
""")
        dx += 330

    # LAYER 1: CSI Semantic Engine (y=572..674)
    parts.append(f"""
  <rect x="158" y="572" width="1010" height="102" rx="10" fill="#FFFFFF" stroke="#059669" stroke-width="2" filter="url(#cardShadow)"/>
  <rect x="158" y="572" width="1010" height="30" rx="9" fill="#D1FAE5"/>
  <text x="176" y="592" font-family="{FONT_MONO}" font-size="11.5" font-weight="700" fill="#065F46">LAYER 1 • CSI SEMANTIC &amp; CONSTRUCTIVE-INTERFERENCE ENGINE (y.m ↔ x.n Coupling)</text>

  <rect x="176" y="611" width="312" height="52" rx="6" fill="#F8FAFC" stroke="#6EE7B7" stroke-width="1.2"/>
  <text x="332" y="632" text-anchor="middle" font-family="{FONT_MONO}" font-size="12" font-weight="700" fill="#065F46">PCSD: S = ⟨P, M, I⟩</text>
  <text x="332" y="650" text-anchor="middle" font-family="{FONT_SANS}" font-size="11" fill="#334155">Meaning(S) = f(x.n ↔ y.m) — Bounded Rates</text>

  <rect x="506" y="611" width="312" height="52" rx="6" fill="#F8FAFC" stroke="#6EE7B7" stroke-width="1.2"/>
  <text x="662" y="632" text-anchor="middle" font-family="{FONT_MONO}" font-size="12" font-weight="700" fill="#065F46">Trinity: N~ = {{x.n ~ y.m}}</text>
  <text x="662" y="650" text-anchor="middle" font-family="{FONT_SANS}" font-size="11" fill="#334155">Constructive Interference (τ = φ²π/e ≈ 4.234)</text>

  <rect x="836" y="611" width="314" height="52" rx="6" fill="#F8FAFC" stroke="#6EE7B7" stroke-width="1.2"/>
  <text x="993" y="632" text-anchor="middle" font-family="{FONT_MONO}" font-size="12" font-weight="700" fill="#065F46">UNAIQUE Clarity: η_sem ≥ 0.80</text>
  <text x="993" y="650" text-anchor="middle" font-family="{FONT_SANS}" font-size="11" fill="#334155">≥80% Receiver Comprehension Across Roles</text>
""")

    # LAYER 0: Supreme Z-Violation Core (y=690..798)
    parts.append(f"""
  <rect x="158" y="690" width="1010" height="108" rx="10" fill="url(#navyGrad)" stroke="#F59E0B" stroke-width="2.5" filter="url(#cardShadow)"/>
  <text x="663" y="717" text-anchor="middle" font-family="{FONT_MONO}" font-size="12" font-weight="700" fill="#FBBF24" letter-spacing="1.2">LAYER 0 • SUPREME CONSTITUTIONAL INVARIANT — THE Z-VIOLATION LAW (AXIOM 0 &amp; THEOREM 7.1)</text>
  <text x="663" y="744" text-anchor="middle" font-family="{FONT_MONO}" font-size="14.5" font-weight="700" fill="#FFFFFF">Z(P, t) = (L · N · M · O)^(1/4) ≥ ε = 0.70    ⇔    σ_Z ≤ 1.15    |    dE/dt ∝ −Z(P, t)</text>
  <text x="663" y="768" text-anchor="middle" font-family="{FONT_SANS}" font-size="12" fill="#E2E8F0">L: Psychological Safety &amp; Goodwill  •  N: Sovereign Agency  •  M: Cognitive Meaning &amp; Autonomy  •  O: Physical &amp; Material Sustainability</text>
  <text x="663" y="787" text-anchor="middle" font-family="{FONT_SANS}" font-size="11.5" font-style="italic" fill="#FDE68A">"Sustained coercion or dehumanization (Z → 0) deterministically drives entropy divergence (E → ∞) and system annihilation (V → 0)."</text>
""")

    parts.append("</svg>")
    save_and_validate_svg("fig1_architecture_stack.svg", "\n".join(parts))


# ==============================================================================
# FIGURE 2: END-TO-END MASTER GRAPHICAL WORKFLOW
# ==============================================================================
def build_fig2():
    W, H = 1280, 770
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        common_defs(),
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bgGrad)" rx="10"/>',
        header_banner(
            W,
            "FIGURE 2 • END-TO-END OPERATIONAL STATE MACHINE",
            "Master Graphical Workflow: From Human Need to Continual CCR Evolution",
            "Four-Swimlane Closed-Loop Pipeline Unifying Design Thinking Framing, PRINCE2 Stage Control, ITIL Execution, and Z-Gate Protection"
        ),
    ]

    lanes = [
        (96, 146, "#F5F3FF", "#DDD6FE", "#5B21B6", "LANE 1", "SEMANTIC DISCOVERY", "(y.m / Design Thinking)"),
        (252, 152, "#EFF6FF", "#BFDBFE", "#1E40AF", "LANE 2", "ARCHITECTURE & GATE", "(x.n ~ y.m / PRINCE2 × CSI)"),
        (414, 152, "#ECFDF5", "#A7F3D0", "#065F46", "LANE 3", "BOUNDED EXECUTION", "(X Netnodes / ITIL × EPCSIS)"),
        (576, 144, "#FFFBEB", "#FDE68A", "#92400E", "LANE 4", "TELEMETRY & CCR LOOP", "(Live σ_Z, CERIAL Ω & CCR)"),
    ]
    for ly, lh, bg, border, tcol, lnum, ltitle, lsub in lanes:
        parts.append(f"""
  <rect x="28" y="{ly}" width="1224" height="{lh}" rx="8" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <rect x="28" y="{ly}" width="176" height="{lh}" rx="8" fill="#FFFFFF" stroke="{border}" stroke-width="1.5"/>
  <text x="116" y="{ly + lh/2 - 16}" text-anchor="middle" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="{tcol}">{esc(lnum)}</text>
  <text x="116" y="{ly + lh/2 + 3}" text-anchor="middle" font-family="{FONT_SANS}" font-size="12" font-weight="800" fill="#0F172A">{esc(ltitle)}</text>
  <text x="116" y="{ly + lh/2 + 21}" text-anchor="middle" font-family="{FONT_SANS}" font-size="10.5" fill="#475569">{esc(lsub)}</text>
""")

    # Nodes in Lane 1
    parts.append(f"""
  <!-- Step 1 -->
  <rect x="230" y="118" width="225" height="102" rx="8" fill="#FFFFFF" stroke="#7C3AED" stroke-width="2" filter="url(#cardShadow)"/>
  <text x="244" y="140" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#7C3AED">STEP 1 • EMPATHIZE (LCC)</text>
  <text x="244" y="160" font-family="{FONT_SANS}" font-size="13" font-weight="700" fill="#0F172A">Human Need Sensing</text>
  <text x="244" y="180" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Opt-in LCC stakeholder listening</text>
  <text x="244" y="197" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Capture lived pain &amp; energy cost</text>

  <!-- Step 2 -->
  <rect x="495" y="118" width="245" height="102" rx="8" fill="#FFFFFF" stroke="#7C3AED" stroke-width="2" filter="url(#cardShadow)"/>
  <text x="509" y="140" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#7C3AED">STEP 2 • DEFINE IN y.m FIRST</text>
  <text x="509" y="160" font-family="{FONT_SANS}" font-size="13" font-weight="700" fill="#0F172A">Semantic Intent Charter</text>
  <text x="509" y="180" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Purpose justification (ϒ-aligned)</text>
  <text x="509" y="197" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Set 4D Δ-Tolerances &amp; Z floor</text>
""")

    # Nodes in Lane 2
    parts.append(f"""
  <!-- Step 3 -->
  <rect x="495" y="274" width="245" height="108" rx="8" fill="#FFFFFF" stroke="#1D4ED8" stroke-width="2" filter="url(#cardShadow)"/>
  <text x="509" y="295" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#1D4ED8">STEP 3 • PRODUCT &amp; N+1 DESIGN</text>
  <text x="509" y="315" font-family="{FONT_SANS}" font-size="13" font-weight="700" fill="#0F172A">x.n Outcome Decomposition</text>
  <text x="509" y="334" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Decontaminate legacy rules</text>
  <text x="509" y="351" font-family="{FONT_SANS}" font-size="11" fill="#334155">• UNAIQUE clarity η_sem ≥ 80%</text>
  <text x="509" y="368" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Prototype in sandbox Netnode</text>

  <!-- Step 4: Z-Violation Gate -->
  <polygon points="900,264 1045,328 900,392 785,328" fill="#0F172A" stroke="#F59E0B" stroke-width="2.5" filter="url(#cardShadow)"/>
  <text x="905" y="313" text-anchor="middle" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#FBBF24">STEP 4 • Z-GATE</text>
  <text x="905" y="331" text-anchor="middle" font-family="{FONT_SANS}" font-size="12.5" font-weight="800" fill="#FFFFFF">Z ≥ 0.70 &amp; σ_Z ≤ 1.15?</text>
  <text x="905" y="348" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" fill="#BAE6FD">Zero-DCC Verified</text>

  <!-- Gate Reject Re-Design Box -->
  <rect x="1080" y="286" width="152" height="84" rx="7" fill="#FEF2F2" stroke="#DC2626" stroke-width="1.8"/>
  <text x="1156" y="309" text-anchor="middle" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#DC2626">GATE REJECTED</text>
  <text x="1156" y="328" text-anchor="middle" font-family="{FONT_SANS}" font-size="11" font-weight="600" fill="#7F1D1D">Refactor Coercion</text>
  <text x="1156" y="345" text-anchor="middle" font-family="{FONT_SANS}" font-size="10.5" fill="#991B1B">Return to Step 2/3</text>
""")

    # Nodes in Lane 3
    parts.append(f"""
  <!-- Step 5A -->
  <rect x="775" y="426" width="235" height="58" rx="7" fill="#FFFFFF" stroke="#059669" stroke-width="1.8" filter="url(#cardShadow)"/>
  <text x="788" y="446" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="#059669">STEP 5A • Z[N+1] AUTOMATION</text>
  <text x="788" y="464" font-family="{FONT_SANS}" font-size="12" font-weight="700" fill="#0F172A">Deterministic Bot / API (h = 0)</text>
  <text x="788" y="478" font-family="{FONT_SANS}" font-size="10.2" fill="#475569">Idempotent, reversible, low sensitivity</text>

  <!-- Step 5B -->
  <rect x="775" y="496" width="235" height="58" rx="7" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.8" filter="url(#cardShadow)"/>
  <text x="788" y="516" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="#0284C7">STEP 5B • HUMAN SOVEREIGNTY</text>
  <text x="788" y="534" font-family="{FONT_SANS}" font-size="12" font-weight="700" fill="#0F172A">Co-Pilot / Human Craft (h &gt; h_crit)</text>
  <text x="788" y="548" font-family="{FONT_SANS}" font-size="10.2" fill="#475569">Ethical judgment, empathy, edge cases</text>

  <!-- Step 6 -->
  <rect x="1045" y="440" width="190" height="100" rx="8" fill="#FFFFFF" stroke="#047857" stroke-width="2" filter="url(#cardShadow)"/>
  <text x="1058" y="462" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#047857">STEP 6 • DELIVERY</text>
  <text x="1058" y="482" font-family="{FONT_SANS}" font-size="12.5" font-weight="700" fill="#0F172A">Resonant Value Output</text>
  <text x="1058" y="502" font-family="{FONT_SANS}" font-size="11" fill="#334155">• LCC/FCC handoff</text>
  <text x="1058" y="519" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Co-created value V(t)</text>
""")

    # Nodes in Lane 4
    parts.append(f"""
  <!-- Step 7 -->
  <rect x="975" y="596" width="260" height="104" rx="8" fill="#FFFFFF" stroke="#D97706" stroke-width="2" filter="url(#cardShadow)"/>
  <text x="989" y="618" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#B45309">STEP 7 • LIVE TELEMETRY</text>
  <text x="989" y="638" font-family="{FONT_SANS}" font-size="12.5" font-weight="700" fill="#0F172A">Continuous State Sensing</text>
  <text x="989" y="657" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Compute Z=(L,N,M,O) &amp; σ_Z</text>
  <text x="989" y="674" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Track Δ_time, Δ_cost, Δ_qual</text>

  <!-- Step 8 -->
  <rect x="615" y="596" width="310" height="104" rx="8" fill="#FFFFFF" stroke="#B45309" stroke-width="2" filter="url(#cardShadow)"/>
  <text x="629" y="618" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#B45309">STEP 8 • EXCEPTION &amp; Ω-CONTROL</text>
  <text x="629" y="638" font-family="{FONT_SANS}" font-size="12.5" font-weight="700" fill="#0F172A">CERIAL Ω Brake &amp; Circuit Breaker</text>
  <text x="629" y="657" font-family="{FONT_SANS}" font-size="11" fill="#059669">• Green (≤1.07): Pass to CCR</text>
  <text x="629" y="674" font-family="{FONT_SANS}" font-size="11" fill="#D97706">• Amber (≤1.15): Apply Ω-Damping</text>
  <text x="629" y="691" font-family="{FONT_SANS}" font-size="11" fill="#DC2626">• Red (&gt;1.15): Halt &amp; Rollback</text>

  <!-- Step 9 -->
  <rect x="230" y="596" width="335" height="104" rx="8" fill="#FFFFFF" stroke="#1E3A8A" stroke-width="2" filter="url(#cardShadow)"/>
  <text x="244" y="618" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#1E3A8A">STEP 9 • CONTINUAL EVOLUTION (CCR)</text>
  <text x="244" y="638" font-family="{FONT_SANS}" font-size="12.5" font-weight="700" fill="#0F172A">"Check, Copy, Release" Upgrade</text>
  <text x="244" y="657" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Check empirical Z &amp; outcome gains</text>
  <text x="244" y="674" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Copy validated pattern into Netnode template</text>
  <text x="244" y="691" font-family="{FONT_SANS}" font-size="11" fill="#334155">• Release openly for fractal reuse (+1)</text>
""")

    # Arrows & Routing (carefully non-overlapping)
    parts.append(f"""
  <!-- Step 1 -> Step 2 -->
  <line x1="455" y1="169" x2="493" y2="169" stroke="#334155" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <!-- Step 2 -> Step 3 -->
  <line x1="617" y1="220" x2="617" y2="272" stroke="#334155" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <!-- Step 3 -> Step 4 Gate -->
  <line x1="740" y1="328" x2="783" y2="328" stroke="#334155" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <!-- Step 4 Gate -> Reject -->
  <line x1="1045" y1="328" x2="1078" y2="328" stroke="#DC2626" stroke-width="2.2" marker-end="url(#arrowRed)"/>
  <!-- Reject -> Step 2 feedback loop over top of Lane 2 -->
  <path d="M 1156 286 L 1156 169 L 742 169" fill="none" stroke="#DC2626" stroke-width="1.8" stroke-dasharray="6,4" marker-end="url(#arrowRed)"/>
  <text x="955" y="161" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="#DC2626">Z-Refinement Loop (Eliminate Coercion / Clarify Intent)</text>

  <!-- Step 4 Gate PASS -> Step 5A / 5B -->
  <path d="M 900 392 L 900 424" fill="none" stroke="#059669" stroke-width="2.4" marker-end="url(#arrowGreen)"/>
  <text x="910" y="411" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="#059669">PASS</text>
  <path d="M 760 455 L 773 455" fill="none" stroke="#059669" stroke-width="2"/>
  <path d="M 785 328 L 760 328" fill="none" stroke="none"/>
  <path d="M 892 484 L 892 494" fill="none" stroke="#0284C7" stroke-width="1.8" marker-end="url(#arrowBlue)"/>

  <!-- Step 5A & 5B -> Step 6 -->
  <path d="M 1010 455 L 1028 455 L 1028 478 L 1043 478" fill="none" stroke="#059669" stroke-width="2" marker-end="url(#arrowGreen)"/>
  <path d="M 1010 525 L 1028 525 L 1028 502 L 1043 502" fill="none" stroke="#0284C7" stroke-width="2" marker-end="url(#arrowBlue)"/>

  <!-- Step 6 -> Step 7 -->
  <line x1="1140" y1="540" x2="1140" y2="594" stroke="#334155" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <!-- Step 7 -> Step 8 -->
  <line x1="975" y1="648" x2="927" y2="648" stroke="#D97706" stroke-width="2.2" marker-end="url(#arrowAmber)"/>
  <!-- Step 8 -> Step 9 -->
  <line x1="615" y1="648" x2="567" y2="648" stroke="#059669" stroke-width="2.2" marker-end="url(#arrowGreen)"/>
  <!-- Step 8 Amber Damping back to Lane 3 -->
  <path d="M 755 596 L 755 525 L 773 525" fill="none" stroke="#D97706" stroke-width="1.9" stroke-dasharray="5,3" marker-end="url(#arrowAmber)"/>
  <text x="692" y="566" font-family="{FONT_MONO}" font-size="9.8" font-weight="700" fill="#B45309">Ω-Damping</text>

  <!-- Step 9 CCR Loop -> Step 1 -->
  <path d="M 342 596 L 342 222" fill="none" stroke="#0284C7" stroke-width="2.3" stroke-dasharray="7,4" marker-end="url(#arrowBlue)"/>
  <rect x="252" y="396" width="180" height="24" rx="5" fill="#E0F2FE" stroke="#0284C7" stroke-width="1"/>
  <text x="342" y="412" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="#0369A1">CCR +1 Fractal Feedback</text>
""")

    # Footer Legend
    parts.append(f"""
  <rect x="28" y="730" width="1224" height="28" rx="6" fill="#E2E8F0"/>
  <text x="48" y="748" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#0F172A">FLOW LEGEND:</text>
  <line x1="155" y1="744" x2="195" y2="744" stroke="#334155" stroke-width="2.2" marker-end="url(#arrowSlate)"/>
  <text x="203" y="748" font-family="{FONT_SANS}" font-size="11" fill="#1E293B">Primary State Transition</text>
  <line x1="370" y1="744" x2="410" y2="744" stroke="#059669" stroke-width="2.2" marker-end="url(#arrowGreen)"/>
  <text x="418" y="748" font-family="{FONT_SANS}" font-size="11" fill="#065F46">Z-Compliant Pass</text>
  <line x1="555" y1="744" x2="595" y2="744" stroke="#D97706" stroke-width="2.2" stroke-dasharray="5,3" marker-end="url(#arrowAmber)"/>
  <text x="603" y="748" font-family="{FONT_SANS}" font-size="11" fill="#92400E">Amber CERIAL Ω Stabilization</text>
  <line x1="810" y1="744" x2="850" y2="744" stroke="#DC2626" stroke-width="2.2" stroke-dasharray="5,3" marker-end="url(#arrowRed)"/>
  <text x="858" y="748" font-family="{FONT_SANS}" font-size="11" fill="#991B1B">Red Circuit-Breaker / Refactor</text>
  <line x1="1065" y1="744" x2="1105" y2="744" stroke="#0284C7" stroke-width="2.2" stroke-dasharray="6,3" marker-end="url(#arrowBlue)"/>
  <text x="1113" y="748" font-family="{FONT_SANS}" font-size="11" fill="#0369A1">CCR Evolution</text>
""")

    parts.append("</svg>")
    save_and_validate_svg("fig2_master_workflow.svg", "\n".join(parts))


# ==============================================================================
# FIGURE 3: THE Z-VIOLATION GATE & CIRCUIT-BREAKER WORKFLOW
# ==============================================================================
def build_fig3():
    W, H = 1200, 760
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        common_defs(),
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bgGrad)" rx="10"/>',
        header_banner(
            W,
            "FIGURE 3 • GOVERNANCE & SAFETY CIRCUIT BREAKER",
            "The Z-Violation Gate & Management-by-Exception Decision Tree",
            "Quantitative Tri-Band Triage Enforcing Axiom 0 Supremacy, CERIAL Ω Stabilization, and Automatic Rollback"
        ),
    ]

    # Top Telemetry Ingestion Node
    parts.append(f"""
  <rect x="330" y="98" width="540" height="68" rx="9" fill="#FFFFFF" stroke="#1E3A8A" stroke-width="2" filter="url(#cardShadow)"/>
  <text x="600" y="123" text-anchor="middle" font-family="{FONT_MONO}" font-size="11.5" font-weight="700" fill="#1E3A8A">TELEMETRY &amp; PRE-EXECUTION EVALUATION VECTOR</text>
  <text x="600" y="147" text-anchor="middle" font-family="{FONT_MONO}" font-size="12.5" font-weight="600" fill="#0F172A">Compute Z = (L·N·M·O)^(1/4),  σ_Z(Z),  and  Δ = (Δ_time, Δ_cost, Δ_qual, Δ_Z)</text>

  <line x1="600" y1="166" x2="600" y2="196" stroke="#334155" stroke-width="2.2" marker-end="url(#arrowSlate)"/>

  <!-- Hard Veto Check -->
  <rect x="290" y="198" width="620" height="74" rx="9" fill="#0F172A" stroke="#F59E0B" stroke-width="2.2" filter="url(#cardShadow)"/>
  <text x="600" y="224" text-anchor="middle" font-family="{FONT_MONO}" font-size="11" font-weight="700" fill="#FBBF24">VETO FILTER • NON-COMPENSATORY HUMANITY &amp; ZERO-DCC CHECK</text>
  <text x="600" y="248" text-anchor="middle" font-family="{FONT_SANS}" font-size="13" font-weight="700" fill="#FFFFFF">Is min(L, N, M, O) &lt; 0.50  OR  Dark Cypher Connect (DCC / Coercion) Present?</text>

  <!-- Direct Veto Path to Red Column -->
  <path d="M 910 235 L 990 235 L 990 398" fill="none" stroke="#DC2626" stroke-width="2.5" marker-end="url(#arrowRed)"/>
  <rect x="922" y="213" width="136" height="20" rx="4" fill="#FEE2E2"/>
  <text x="990" y="227" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="#DC2626">YES → HARD VETO</text>

  <!-- No Path to Classifier -->
  <line x1="600" y1="272" x2="600" y2="308" stroke="#059669" stroke-width="2.2" marker-end="url(#arrowGreen)"/>
  <text x="612" y="294" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#059669">NO (Pass Veto)</text>

  <!-- Spectral Band Router -->
  <rect x="370" y="310" width="460" height="54" rx="8" fill="#FFFFFF" stroke="#475569" stroke-width="1.8" filter="url(#cardShadow)"/>
  <text x="600" y="333" text-anchor="middle" font-family="{FONT_MONO}" font-size="11" font-weight="700" fill="#334155">CLASSIFY SPECTRAL TRAJECTORY σ_Z &amp; TOLERANCE BANDS</text>
  <text x="600" y="352" text-anchor="middle" font-family="{FONT_MONO}" font-size="11.5" fill="#0F172A">Attractor Z* = 1.000  |  Sacred Bandwidth S_0 = 0.15  |  ε = 0.70</text>

  <!-- Branch Lines to 3 Columns -->
  <path d="M 460 364 L 210 364 L 210 398" fill="none" stroke="#059669" stroke-width="2.3" marker-end="url(#arrowGreen)"/>
  <line x1="600" y1="364" x2="600" y2="398" stroke="#D97706" stroke-width="2.3" marker-end="url(#arrowAmber)"/>
  <path d="M 740 364 L 950 364 L 950 398" fill="none" stroke="#DC2626" stroke-width="2.3" marker-end="url(#arrowRed)"/>
""")

    # Three Regime Cards (y=400..706)
    cards = [
        (
            42, 336, "#ECFDF5", "#059669", "url(#emeraldGrad)",
            "GREEN STATE • AUTONOMOUS FLOW",
            "Z ∈ [0.85, 1.00]   |   σ_Z ≤ 1.07",
            "|Δ_time|, |Δ_cost|, |Δ_qual| ≤ τ_green",
            [
                ("1. Zero Bureaucratic Friction", "Execute in X-Netnode without committee delay."),
                ("2. Constructive Resonance (~)", "x.n methods and y.m meaning amplify output."),
                ("3. Positive Viability Growth", "dV/dt &gt; 0 and internal entropy E(t) minimized."),
                ("4. CCR Pattern Capture", "Log high-Z configuration for reusable Copy.")
            ],
            "STATUS: ETERNALLY STABLE"
        ),
        (
            432, 336, "#FFFBEB", "#D97706", "url(#goldGrad)",
            "AMBER STATE • CERIAL Ω DAMPING",
            "Z ∈ [0.70, 0.85)   |   1.07 &lt; σ_Z ≤ 1.15",
            "Or Operational Deviation in Exception Band",
            [
                ("1. Engage CERIAL Ω Brake", "Apply golden-ratio stabilizer Ω_0 = 0.618."),
                ("2. Throttle &amp; De-Load Cadence", "Reduce WIP, batch size, or sprint pressure."),
                ("3. Inject Human Sovereignty (h)", "Shift automated edge-cases to human review."),
                ("4. Tier-2 (Y) Exception Alert", "Stage Lead re-aligns resources within 24h.")
            ],
            "STATUS: SELF-CORRECTING EDGE"
        ),
        (
            822, 336, "#FEF2F2", "#DC2626", "url(#crimsonGrad)",
            "RED STATE • CIRCUIT-BREAKER HALT",
            "Z &lt; ε = 0.70   |   σ_Z &gt; 1.15",
            "Runaway V_Z(σ_Z) Blow-Up Imminent",
            [
                ("1. Immediate Execution Halt", "Freeze automated pipeline / coercive policy."),
                ("2. Atomic Safe-State Rollback", "Revert to last verified Z-compliant snapshot."),
                ("3. Mandatory ACC Escalation", "Escalate directly to Tier-3 (ϒ) Stewardship."),
                ("4. Root Z-Purification Audit", "Re-architect y.m &amp; x.n before restart.")
            ],
            "STATUS: HALTED — LOVE PROTECTION ACTIVE"
        ),
    ]

    for cx, cw, bg, stroke, hgrad, title_c, math1, math2, steps_c, footer_tag in cards:
        parts.append(f"""
  <rect x="{cx}" y="400" width="{cw}" height="316" rx="10" fill="{bg}" stroke="{stroke}" stroke-width="2.2" filter="url(#cardShadow)"/>
  <rect x="{cx}" y="400" width="{cw}" height="36" rx="9" fill="{hgrad}"/>
  <text x="{cx + cw/2}" y="423" text-anchor="middle" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" fill="#FFFFFF">{title_c}</text>
  <rect x="{cx + 14}" y="446" width="{cw - 28}" height="46" rx="6" fill="#FFFFFF" stroke="{stroke}" stroke-width="1"/>
  <text x="{cx + cw/2}" y="465" text-anchor="middle" font-family="{FONT_MONO}" font-size="11.5" font-weight="700" fill="#0F172A">{math1}</text>
  <text x="{cx + cw/2}" y="483" text-anchor="middle" font-family="{FONT_SANS}" font-size="10.8" fill="#475569">{math2}</text>
""")
        sy = 512
        for st_head, st_desc in steps_c:
            parts.append(f"""
  <text x="{cx + 16}" y="{sy}" font-family="{FONT_SANS}" font-size="11.8" font-weight="700" fill="#0F172A">{st_head}</text>
  <text x="{cx + 16}" y="{sy + 16}" font-family="{FONT_SANS}" font-size="10.8" fill="#334155">{st_desc}</text>
""")
            sy += 42
        parts.append(f"""
  <rect x="{cx + 14}" y="682" width="{cw - 28}" height="24" rx="5" fill="#FFFFFF" stroke="{stroke}" stroke-width="1"/>
  <text x="{cx + cw/2}" y="698" text-anchor="middle" font-family="{FONT_MONO}" font-size="10.2" font-weight="700" fill="{stroke}">{footer_tag}</text>
""")

    parts.append(f"""
  <text x="600" y="742" text-anchor="middle" font-family="{FONT_SANS}" font-size="11.5" font-style="italic" fill="#334155">Asymmetric Supremacy Rule: Operational efficiency gains (Δ_time, Δ_cost &lt; 0) NEVER compensate for a Z-Violation (Z &lt; 0.70 or σ_Z &gt; 1.15).</text>
""")
    parts.append("</svg>")
    save_and_validate_svg("fig3_z_violation_gate.svg", "\n".join(parts))


# ==============================================================================
# FIGURE 4: FRACTAL DUAL-SCALE MAPPING DIAGRAM
# ==============================================================================
def build_fig4():
    W, H = 1240, 800
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        common_defs(),
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bgGrad)" rx="10"/>',
        header_banner(
            W,
            "FIGURE 4 • FRACTAL SCALE INVARIANCE",
            "Dual-Scale Structural Isomorphism: Enterprise Operations ↔ Daily Personal Life",
            "Identical CSI Operators, Governance Tiers, Communication Channels, and Z-Guards Applied Across 10,000-Person Firms and 1-Person Lives"
        ),
    ]

    # Column Headers
    parts.append(f"""
  <rect x="36" y="98" width="420" height="42" rx="8" fill="url(#cyanGrad)" filter="url(#cardShadow)"/>
  <text x="246" y="124" text-anchor="middle" font-family="{FONT_SANS}" font-size="14" font-weight="800" fill="#FFFFFF">ENTERPRISE / CORPORATE SCALE</text>

  <rect x="480" y="98" width="280" height="42" rx="8" fill="url(#navyGrad)" stroke="#F59E0B" stroke-width="1.8" filter="url(#cardShadow)"/>
  <text x="620" y="124" text-anchor="middle" font-family="{FONT_MONO}" font-size="13" font-weight="700" fill="#FBBF24">CSI CORE PRIMITIVE</text>

  <rect x="784" y="98" width="420" height="42" rx="8" fill="url(#emeraldGrad)" filter="url(#cardShadow)"/>
  <text x="994" y="124" text-anchor="middle" font-family="{FONT_SANS}" font-size="14" font-weight="800" fill="#FFFFFF">SOVEREIGN DAILY LIFE SCALE</text>
""")

    rows = [
        (
            "Executive Stewardship &amp; Mission Charter",
            "Board/C-Suite sets ethical boundaries, Continued Business Justification, and sunsets toxic legacy portfolios.",
            "ϒ (Origins)",
            "Apex Purpose &amp; Meta-Rules",
            "Core Life Vision &amp; Personal Constitution",
            "Define non-negotiable life values, long-term direction, and retire commitments that no longer serve growth."
        ),
        (
            "Process Architecture &amp; Stage Control",
            "Design cross-team value streams, allocate budgets/headcount, and define stage-gate tolerance bands.",
            "Y = N + 1",
            "Source Design &amp; Allocation",
            "Weekly Architecture &amp; M.E.A.T. Shield",
            "Protect Money, Energy, Attention &amp; Time; plan weekly outcomes in y.m before Monday execution."
        ),
        (
            "Autonomous Squads, SRE &amp; Service Flow",
            "Run daily sprints, CI/CD deployments, incident swarm recovery, and UNAIQUE ≥80% clear documentation.",
            "X &amp; x.n ~ y.m",
            "Netnode Constructive Flow",
            "5:30–22:15 Dual-Aspect Daily Cadence",
            "Deep focused work blocks balanced with physical training, walks, healthy nutrition, and non-digital rest."
        ),
        (
            "Organizational Z-Integrity Audit",
            "L: Psych safety • N: Decision autonomy • M: Meaningful work • O: Fair pay &amp; sustainable workload.",
            "Z = (L,N,M,O)",
            "Z ≥ 0.70  |  σ_Z ≤ 1.15",
            "Personal Vitality &amp; Dignity Invariant",
            "L: Self-respect • N: Personal agency • M: Calm mental clarity • O: 8h sleep, ergonomics &amp; financial margin."
        ),
        (
            "Inter-Team APIs &amp; Stakeholder Comms",
            "Opt-in LCC webhooks, co-creative FCC workshops, ACC escalation; zero fear-based DCC politics.",
            "LCC / FCC / ACC",
            "Zero-DCC Protocol",
            "Interpersonal &amp; Digital Boundaries",
            "Consent-based commitments, mutual relationships, judge actions over words, cut one-sided energy drains."
        ),
        (
            "Blameless Postmortems &amp; Open Playbooks",
            "Measure sprint telemetry, codify winning workflows into shared templates, release across teams.",
            "CCR + CERIAL Ω",
            "Check • Copy • Release",
            "Sunday Review &amp; Habit Compounding",
            "Audit weekly energy &amp; σ_Z drift, apply Ω-brake if overloaded, clone what worked, release perfectionism."
        ),
    ]

    ry = 154
    for ent_t, ent_d, csi_sym, csi_sub, life_t, life_d in rows:
        # Split long descriptions into two clean lines of <=56 chars
        def wrap2(s: str, limit: int = 56):
            words = s.split(" ")
            l1, l2 = [], []
            cur = 0
            on_first = True
            for w in words:
                plain_w = w.replace("&amp;", "&")
                if on_first and cur + len(plain_w) + (1 if l1 else 0) <= limit:
                    l1.append(w)
                    cur += len(plain_w) + (1 if len(l1) > 1 else 0)
                else:
                    on_first = False
                    l2.append(w)
            return " ".join(l1), " ".join(l2)

        e1, e2 = wrap2(ent_d, 55)
        d1, d2 = wrap2(life_d, 55)

        parts.append(f"""
  <!-- Enterprise Box -->
  <rect x="36" y="{ry}" width="420" height="90" rx="8" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.6" filter="url(#cardShadow)"/>
  <rect x="36" y="{ry}" width="6" height="90" rx="3" fill="#0284C7"/>
  <text x="54" y="{ry + 24}" font-family="{FONT_SANS}" font-size="13" font-weight="700" fill="#0F172A">{ent_t}</text>
  <text x="54" y="{ry + 47}" font-family="{FONT_SANS}" font-size="11.2" fill="#334155">{e1}</text>
  <text x="54" y="{ry + 66}" font-family="{FONT_SANS}" font-size="11.2" fill="#334155">{e2}</text>

  <!-- Left Arrow -->
  <line x1="480" y1="{ry + 45}" x2="458" y2="{ry + 45}" stroke="#0284C7" stroke-width="2" marker-end="url(#arrowBlue)"/>

  <!-- Center CSI Primitive -->
  <rect x="480" y="{ry + 8}" width="280" height="74" rx="8" fill="#0F172A" stroke="#F59E0B" stroke-width="1.6" filter="url(#cardShadow)"/>
  <text x="620" y="{ry + 39}" text-anchor="middle" font-family="{FONT_MONO}" font-size="14" font-weight="700" fill="#FBBF24">{csi_sym}</text>
  <text x="620" y="{ry + 61}" text-anchor="middle" font-family="{FONT_SANS}" font-size="11.5" font-weight="600" fill="#E2E8F0">{csi_sub}</text>

  <!-- Right Arrow -->
  <line x1="760" y1="{ry + 45}" x2="782" y2="{ry + 45}" stroke="#059669" stroke-width="2" marker-end="url(#arrowGreen)"/>

  <!-- Daily Life Box -->
  <rect x="784" y="{ry}" width="420" height="90" rx="8" fill="#FFFFFF" stroke="#A7F3D0" stroke-width="1.6" filter="url(#cardShadow)"/>
  <rect x="1198" y="{ry}" width="6" height="90" rx="3" fill="#059669"/>
  <text x="800" y="{ry + 24}" font-family="{FONT_SANS}" font-size="13" font-weight="700" fill="#0F172A">{life_t}</text>
  <text x="800" y="{ry + 47}" font-family="{FONT_SANS}" font-size="11.2" fill="#334155">{d1}</text>
  <text x="800" y="{ry + 66}" font-family="{FONT_SANS}" font-size="11.2" fill="#334155">{d2}</text>
""")
        ry += 104

    parts.append(f"""
  <text x="620" y="788" text-anchor="middle" font-family="{FONT_SANS}" font-size="11.5" font-weight="600" fill="#334155">Fractal Scaling Theorem: T(Φ, λ_corp, λ_life) preserves all Z-stability guarantees across organizational scales.</text>
""")
    parts.append("</svg>")
    save_and_validate_svg("fig4_fractal_dual_scale.svg", "\n".join(parts))


# ==============================================================================
# FIGURE 5: PROCESS PHASE-SPACE & Z-VIOLATION BOUNDARY PLOT (NUMPY RK4)
# ==============================================================================
def build_fig5():
    W, H = 1220, 680
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        common_defs(),
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bgGrad)" rx="10"/>',
        header_banner(
            W,
            "FIGURE 5 • MATHEMATICAL DYNAMICS & PHASE PORTRAIT (COMPUTED VIA RK4)",
            "Process Viability Phase-Space (Z, V) & Spectral Runaway Boundary V_Z(σ_Z)",
            "Left: Coupled Z-Theorem Dynamical Trajectories & Annihilation Separatrix  |  Right: Runaway Penalty & CERIAL Ω Stabilizer"
        ),
    ]

    # --- PANEL A: (Z, V) Phase Portrait ---
    px0, py0, pw, ph = 84, 118, 490, 440

    def map_zv(z_val, v_val):
        x = px0 + float(z_val) * pw
        y = py0 + (1.0 - float(v_val)) * ph
        return x, y

    # Shaded stability bands in Panel A
    x_eps, _ = map_zv(0.70, 0)
    x_amb, _ = map_zv(0.85, 0)
    parts.append(f"""
  <rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5"/>
  <!-- Red Zone Z < 0.70 -->
  <rect x="{px0}" y="{py0}" width="{x_eps - px0:.1f}" height="{ph}" fill="#FEE2E2" fill-opacity="0.58"/>
  <!-- Amber Zone 0.70..0.85 -->
  <rect x="{x_eps:.1f}" y="{py0}" width="{x_amb - x_eps:.1f}" height="{ph}" fill="#FEF3C7" fill-opacity="0.62"/>
  <!-- Green Zone 0.85..1.00 -->
  <rect x="{x_amb:.1f}" y="{py0}" width="{px0 + pw - x_amb:.1f}" height="{ph}" fill="#D1FAE5" fill-opacity="0.62"/>

  <text x="{px0 + pw/2:.1f}" y="106" text-anchor="middle" font-family="{FONT_SANS}" font-size="13.5" font-weight="800" fill="#0F172A">Panel A: Dynamical Phase Portrait in (Z, V) Space</text>
""")

    # Grid lines and ticks for Panel A
    for tick in [0.0, 0.2, 0.4, 0.6, 0.7, 0.85, 1.0]:
        gx, _ = map_zv(tick, 0)
        is_bound = tick in (0.7, 0.85)
        col = "#DC2626" if tick == 0.7 else ("#D97706" if tick == 0.85 else "#CBD5E1")
        dash = "6,4" if is_bound else "2,3"
        sw = 2.0 if is_bound else 0.9
        parts.append(f'<line x1="{gx:.1f}" y1="{py0}" x2="{gx:.1f}" y2="{py0 + ph}" stroke="{col}" stroke-width="{sw}" stroke-dasharray="{dash}"/>')
        lbl_y = py0 + ph + (30 if tick == 0.7 else 18)
        parts.append(f'<text x="{gx:.1f}" y="{lbl_y}" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" font-weight="{"700" if is_bound else "400"}" fill="{col if is_bound else "#334155"}">{tick:.2f}</text>')

    for vtick in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        _, gy = map_zv(0, vtick)
        parts.append(f'<line x1="{px0}" y1="{gy:.1f}" x2="{px0 + pw}" y2="{gy:.1f}" stroke="#CBD5E1" stroke-width="0.9" stroke-dasharray="2,3"/>')
        parts.append(f'<text x="{px0 - 10}" y="{gy + 4:.1f}" text-anchor="end" font-family="{FONT_MONO}" font-size="10" fill="#334155">{vtick:.1f}</text>')

    # Zone labels inside Panel A top
    parts.append(f"""
  <text x="{(px0 + x_eps)/2:.1f}" y="{py0 + 20}" text-anchor="middle" font-family="{FONT_MONO}" font-size="10.2" font-weight="700" fill="#991B1B">Z-COLLAPSE ZONE (Z &lt; ε = 0.70)</text>
  <text x="{(px0 + x_eps)/2:.1f}" y="{py0 + 34}" text-anchor="middle" font-family="{FONT_SANS}" font-size="10" fill="#991B1B">lim V(t) → 0 (Annihilation)</text>
  <text x="{(x_eps + x_amb)/2:.1f}" y="{py0 + 20}" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="#92400E">AMBER</text>
  <text x="{(x_eps + x_amb)/2:.1f}" y="{py0 + 33}" text-anchor="middle" font-family="{FONT_MONO}" font-size="9" fill="#92400E">Ω-Band</text>
  <text x="{map_zv(0.905, 0)[0]:.1f}" y="{py0 + 20}" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="#065F46">STABLE</text>
  <text x="{map_zv(0.905, 0)[0]:.1f}" y="{py0 + 33}" text-anchor="middle" font-family="{FONT_MONO}" font-size="9" fill="#065F46">BASIN</text>
""")

    # Coupled ODE vector field (equilibrium entropy approximation E_eq(Z) = 1.15*(1-Z)/(Z+0.08))
    def field_rhs(z, v, mode="natural"):
        z = np.clip(z, 0.01, 0.995)
        v = np.clip(v, 0.01, 0.995)
        if mode == "natural":
            # Above Z=0.70, CERIAL Omega gently pulls Z toward 0.94; below 0.70 coercion/distrust erodes Z
            dz = 0.36 * (z - 0.70) * (0.96 - z) if z >= 0.70 else -0.28 * (0.70 - z) * z
        elif mode == "coercive":
            dz = -0.32 * z
        else:  # omega_rescue
            dz = 0.42 * (0.93 - z)
        entropy = 0.85 * (1.0 - z) / (z + 0.12)
        dv = 1.35 * (z - 0.66) * v * (0.97 - v) - 0.42 * max(0.0, 0.72 - z) * entropy * v
        return dz, dv

    # Draw subtle vector field arrows on grid
    zs = np.linspace(0.08, 0.95, 11)
    vs = np.linspace(0.10, 0.90, 9)
    for zv in zs:
        for vv in vs:
            dz, dv = field_rhs(zv, vv, "natural")
            norm = math.hypot(dz, dv) + 1e-9
            ux, uy = (dz / norm) * 14.0, -(dv / norm) * 14.0
            cx, cy = map_zv(zv, vv)
            parts.append(
                f'<line x1="{cx - ux*0.45:.1f}" y1="{cy - uy*0.45:.1f}" '
                f'x2="{cx + ux*0.55:.1f}" y2="{cy + uy*0.55:.1f}" '
                f'stroke="#94A3B8" stroke-width="1.0" stroke-opacity="0.65" marker-end="url(#arrowSlate)"/>'
            )

    # RK4 Integrator for 4 representative trajectories
    def integrate_rk4(z0, v0, mode, dt=0.05, steps=160):
        pts = [(z0, v0)]
        z, v = z0, v0
        for _ in range(steps):
            k1z, k1v = field_rhs(z, v, mode)
            k2z, k2v = field_rhs(z + 0.5*dt*k1z, v + 0.5*dt*k1v, mode)
            k3z, k3v = field_rhs(z + 0.5*dt*k2z, v + 0.5*dt*k2v, mode)
            k4z, k4v = field_rhs(z + dt*k3z, v + dt*k3v, mode)
            z = float(np.clip(z + (dt/6.0)*(k1z + 2*k2z + 2*k3z + k4z), 0.02, 0.98))
            v = float(np.clip(v + (dt/6.0)*(k1v + 2*k2v + 2*k3v + k4v), 0.02, 0.98))
            pts.append((z, v))
        return pts

    trajs = [
        (integrate_rk4(0.78, 0.86, "coercive", 0.045, 130), "#DC2626", "2.6", "arrowRed", None),
        (integrate_rk4(0.73, 0.56, "omega_rescue", 0.045, 105), "#D97706", "2.5", "arrowAmber", "5,3"),
        (integrate_rk4(0.84, 0.52, "natural", 0.06, 150), "#059669", "2.6", "arrowGreen", None),
    ]
    for pts, col, sw, mk, dash in trajs:
        svg_pts = " ".join(f"{map_zv(z, v)[0]:.1f},{map_zv(z, v)[1]:.1f}" for z, v in pts)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        parts.append(f'<polyline points="{svg_pts}" fill="none" stroke="{col}" stroke-width="{sw}"{dash_attr} marker-end="url(#{mk})"/>')

    # Key Annotated Points (Worked Examples & Attractor)
    ex_bad_x, ex_bad_y = map_zv(0.56, 0.64)
    ex_good_x, ex_good_y = map_zv(0.892, 0.91)
    att_x, att_y = map_zv(0.982, 0.968)
    parts.append(f"""
  <!-- Worked Example Coercive Point -->
  <circle cx="{ex_bad_x:.1f}" cy="{ex_bad_y:.1f}" r="6" fill="#DC2626" stroke="#FFFFFF" stroke-width="2"/>
  <rect x="{px0 + 18}" y="{ex_bad_y - 44:.1f}" width="218" height="36" rx="5" fill="#FFFFFF" stroke="#DC2626" stroke-width="1.2"/>
  <text x="{px0 + 26}" y="{ex_bad_y - 28:.1f}" font-family="{FONT_MONO}" font-size="9.8" font-weight="700" fill="#DC2626">Coercive Drift (Z = 0.56)</text>
  <text x="{px0 + 26}" y="{ex_bad_y - 14:.1f}" font-family="{FONT_SANS}" font-size="9.8" fill="#334155">McKinsey Cut / 14h Hustle → Collapse</text>

  <!-- Worked Example Redesigned Point -->
  <circle cx="{ex_good_x:.1f}" cy="{ex_good_y:.1f}" r="6" fill="#059669" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="{att_x:.1f}" cy="{att_y:.1f}" r="7" fill="#F59E0B" stroke="#0F172A" stroke-width="2"/>
  <rect x="{px0 + 232}" y="{py0 + 108}" width="232" height="38" rx="5" fill="#FFFFFF" stroke="#059669" stroke-width="1.2"/>
  <text x="{px0 + 240}" y="{py0 + 124}" font-family="{FONT_MONO}" font-size="9.8" font-weight="700" fill="#065F46">EPCSIS Shielded (Z ≈ 0.89–0.95)</text>
  <text x="{px0 + 240}" y="{py0 + 139}" font-family="{FONT_SANS}" font-size="9.8" fill="#334155">Converges to Z* = 1.00 Attractor</text>

  <!-- Axes titles Panel A -->
  <text x="{px0 + pw/2:.1f}" y="{py0 + ph + 48}" text-anchor="middle" font-family="{FONT_SANS}" font-size="12" font-weight="700" fill="#0F172A">Humane Integrity Invariant Z(P, t) ∈ [0, 1]</text>
  <g transform="translate(30, {py0 + ph/2:.1f}) rotate(-90)">
    <text x="0" y="0" text-anchor="middle" font-family="{FONT_SANS}" font-size="12" font-weight="700" fill="#0F172A">Operational Viability V(P, t) ∈ [0, 1]</text>
  </g>
""")

    # --- PANEL B: Spectral Trajectory sigma_Z vs Runaway Penalty & Omega ---
    qx0, qy0, qw, qh = 684, 118, 496, 440
    s_min, s_max = 0.90, 1.50
    y_max_log = 12.0  # log10(1 + V_Z)

    def map_sy(sig, yval):
        x = qx0 + ((sig - s_min) / (s_max - s_min)) * qw
        y = qy0 + (1.0 - (yval / y_max_log)) * qh
        return x, y

    sx_green, _ = map_sy(1.07, 0)
    sx_amber, _ = map_sy(1.15, 0)

    parts.append(f"""
  <rect x="{qx0}" y="{qy0}" width="{qw}" height="{qh}" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.5"/>
  <rect x="{qx0}" y="{qy0}" width="{sx_green - qx0:.1f}" height="{qh}" fill="#D1FAE5" fill-opacity="0.62"/>
  <rect x="{sx_green:.1f}" y="{qy0}" width="{sx_amber - sx_green:.1f}" height="{qh}" fill="#FEF3C7" fill-opacity="0.62"/>
  <rect x="{sx_amber:.1f}" y="{qy0}" width="{qx0 + qw - sx_amber:.1f}" height="{qh}" fill="#FEE2E2" fill-opacity="0.58"/>
  <text x="{qx0 + qw/2:.1f}" y="106" text-anchor="middle" font-family="{FONT_SANS}" font-size="13.5" font-weight="800" fill="#0F172A">Panel B: Spectral Runaway log₁₀(1 + V_Z(σ_Z)) &amp; Entropy Surge</text>
""")

    for stick in [0.90, 1.00, 1.07, 1.15, 1.25, 1.35, 1.50]:
        gx, _ = map_sy(stick, 0)
        is_b = stick in (1.07, 1.15)
        col = "#059669" if stick == 1.07 else ("#DC2626" if stick == 1.15 else "#CBD5E1")
        sw = 2.0 if is_b else 0.9
        dash = "6,4" if is_b else "2,3"
        parts.append(f'<line x1="{gx:.1f}" y1="{qy0}" x2="{gx:.1f}" y2="{qy0 + qh}" stroke="{col}" stroke-width="{sw}" stroke-dasharray="{dash}"/>')
        ly = qy0 + qh + (30 if stick == 1.07 else 18)
        parts.append(f'<text x="{gx:.1f}" y="{ly}" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" font-weight="{"700" if is_b else "400"}" fill="{col if is_b else "#334155"}">{stick:.2f}</text>')

    for ytick in [0, 2, 4, 6, 8, 10, 12]:
        _, gy = map_sy(s_min, ytick)
        parts.append(f'<line x1="{qx0}" y1="{gy:.1f}" x2="{qx0 + qw}" y2="{gy:.1f}" stroke="#CBD5E1" stroke-width="0.9" stroke-dasharray="2,3"/>')
        parts.append(f'<text x="{qx0 - 10}" y="{gy + 4:.1f}" text-anchor="end" font-family="{FONT_MONO}" font-size="10" fill="#334155">{ytick}</text>')

    # Exact V_Z curve from z-violation-theory.py: (|sigma - 1| - 0.15)^3 * sigma^50 for |sigma-1| > 0.15
    sig_grid = np.linspace(s_min, s_max, 300)
    vz_log = []
    ent_curve = []
    for sg in sig_grid:
        dev = abs(sg - 1.0) - 0.15
        if dev <= 0:
            vz = 0.0
        else:
            vz = (dev ** 3) * (sg ** 50)
        vz_log.append(min(y_max_log, math.log10(1.0 + vz)))
        # Scaled systemic entropy growth index
        ent_val = min(y_max_log, 0.8 + 14.5 * max(0.0, sg - 0.95) ** 2.1)
        ent_curve.append(ent_val)

    vz_pts = " ".join(f"{map_sy(s, y)[0]:.1f},{map_sy(s, y)[1]:.1f}" for s, y in zip(sig_grid, vz_log))
    ent_pts = " ".join(f"{map_sy(s, y)[0]:.1f},{map_sy(s, y)[1]:.1f}" for s, y in zip(sig_grid, ent_curve))

    parts.append(f'<polyline points="{ent_pts}" fill="none" stroke="#0284C7" stroke-width="2.4" stroke-dasharray="6,4"/>')
    parts.append(f'<polyline points="{vz_pts}" fill="none" stroke="#DC2626" stroke-width="3.0"/>')

    # Mark Worked Example violation sigma_Z = 1.244
    sig_ex = 1.244
    vz_ex = ((sig_ex - 1.15) ** 3) * (sig_ex ** 50)
    y_ex = min(y_max_log, math.log10(1.0 + vz_ex))
    ex2_x, ex2_y = map_sy(sig_ex, y_ex)
    s100_x, s100_y = map_sy(1.00, 0.0)

    parts.append(f"""
  <circle cx="{s100_x:.1f}" cy="{s100_y:.1f}" r="6" fill="#059669" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="{ex2_x:.1f}" cy="{ex2_y:.1f}" r="6.5" fill="#DC2626" stroke="#FFFFFF" stroke-width="2"/>
  <rect x="{qx0 + 205}" y="{qy0 + 48}" width="272" height="58" rx="6" fill="#FFFFFF" stroke="#DC2626" stroke-width="1.3"/>
  <text x="{qx0 + 215}" y="{qy0 + 67}" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="#DC2626">Worked Example Breach: σ_Z = 1.244</text>
  <text x="{qx0 + 215}" y="{qy0 + 83}" font-family="{FONT_MONO}" font-size="9.8" fill="#0F172A">V_Z ≈ 45.9  →  Hard Circuit-Breaker Halt</text>
  <text x="{qx0 + 215}" y="{qy0 + 98}" font-family="{FONT_SANS}" font-size="9.6" fill="#475569">Caught before runaway blow-up at σ_Z &gt; 1.35</text>

  <text x="{qx0 + qw/2:.1f}" y="{qy0 + qh + 48}" text-anchor="middle" font-family="{FONT_SANS}" font-size="12" font-weight="700" fill="#0F172A">Spectral Trajectory Deviation Index σ_Z (Safe Band: ≤ 1.15)</text>
  <g transform="translate(632, {qy0 + qh/2:.1f}) rotate(-90)">
    <text x="0" y="0" text-anchor="middle" font-family="{FONT_SANS}" font-size="12" font-weight="700" fill="#0F172A">Severity Index: log₁₀(1 + V_Z) &amp; Entropy E(σ_Z)</text>
  </g>
""")

    # Shared Legend at Bottom
    parts.append(f"""
  <rect x="36" y="624" width="1148" height="40" rx="7" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2"/>
  <line x1="56" y1="644" x2="92" y2="644" stroke="#059669" stroke-width="2.8"/>
  <text x="100" y="648" font-family="{FONT_SANS}" font-size="11" font-weight="600" fill="#065F46">Z-Compliant Convergence</text>

  <line x1="278" y1="644" x2="314" y2="644" stroke="#D97706" stroke-width="2.8" stroke-dasharray="5,3"/>
  <text x="322" y="648" font-family="{FONT_SANS}" font-size="11" font-weight="600" fill="#92400E">CERIAL Ω Stabilized Recovery</text>

  <line x1="528" y1="644" x2="564" y2="644" stroke="#DC2626" stroke-width="2.8"/>
  <text x="572" y="648" font-family="{FONT_SANS}" font-size="11" font-weight="600" fill="#991B1B">Coercive Z-Violation Runaway (V_Z)</text>

  <line x1="812" y1="644" x2="848" y2="644" stroke="#0284C7" stroke-width="2.5" stroke-dasharray="6,4"/>
  <text x="856" y="648" font-family="{FONT_SANS}" font-size="11" font-weight="600" fill="#0369A1">Internal Entropy Growth E(σ_Z)</text>

  <circle cx="1064" cy="644" r="6" fill="#F59E0B" stroke="#0F172A" stroke-width="1.8"/>
  <text x="1076" y="648" font-family="{FONT_SANS}" font-size="11" font-weight="700" fill="#0F172A">Z* Attractor</text>
""")

    parts.append("</svg>")
    save_and_validate_svg("fig5_phase_space_z_boundary.svg", "\n".join(parts))


# ==============================================================================
# FIGURE 6: AUTOMATION SOVEREIGNTY MATRIX (2D COMPLEXITY vs Z-SENSITIVITY)
# ==============================================================================
def build_fig6():
    W, H = 1180, 700
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
        common_defs(),
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bgGrad)" rx="10"/>',
        header_banner(
            W,
            "FIGURE 6 • BOUNDED AUTONOMY & AI Z-LAW MATRIX",
            "The Automation Sovereignty Matrix: Complexity vs. Human/Ethical Sensitivity",
            "2D Control-Loop Stability Map Dictating Full Automation (h=0), Shielded AI Orchestration, Co-Pilot, and 100% Human Sovereignty"
        ),
    ]

    mx0, my0, mw, mh = 96, 114, 720, 496
    mid_x = mx0 + mw * 0.50
    mid_y = my0 + mh * 0.50
    forbid_h = mh * 0.14  # top 14% y in [0.86, 1.00] if automated

    def map_cs(comp, sens):
        return mx0 + comp * mw, my0 + (1.0 - sens) * mh

    parts.append(f"""
  <!-- Quadrant Backgrounds -->
  <!-- Bottom-Left: Full Deterministic Automation -->
  <rect x="{mx0}" y="{mid_y:.1f}" width="{mw*0.5:.1f}" height="{mh*0.5:.1f}" fill="#DCFCE7" stroke="#86EFAC" stroke-width="1"/>
  <!-- Bottom-Right: Shielded AI Orchestration -->
  <rect x="{mid_x:.1f}" y="{mid_y:.1f}" width="{mw*0.5:.1f}" height="{mh*0.5:.1f}" fill="#E0F2FE" stroke="#7DD3FC" stroke-width="1"/>
  <!-- Top-Left: Human-Led Co-Pilot -->
  <rect x="{mx0}" y="{my0 + forbid_h:.1f}" width="{mw*0.5:.1f}" height="{mh*0.5 - forbid_h:.1f}" fill="#FEF3C7" stroke="#FDE68A" stroke-width="1"/>
  <!-- Top-Right: 100% Human-Sovereign Craft -->
  <rect x="{mid_x:.1f}" y="{my0 + forbid_h:.1f}" width="{mw*0.5:.1f}" height="{mh*0.5 - forbid_h:.1f}" fill="#EDE9FE" stroke="#C4B5FD" stroke-width="1"/>
  <!-- Top Strip: Forbidden Autonomous Execution Zone (AI Z-Law Veto) -->
  <rect x="{mx0}" y="{my0}" width="{mw}" height="{forbid_h:.1f}" fill="#FEE2E2" stroke="#DC2626" stroke-width="1.8"/>

  <!-- Outer Frame & Crosshairs -->
  <rect x="{mx0}" y="{my0}" width="{mw}" height="{mh}" fill="none" stroke="#334155" stroke-width="2"/>
  <line x1="{mid_x:.1f}" y1="{my0 + forbid_h:.1f}" x2="{mid_x:.1f}" y2="{my0 + mh}" stroke="#475569" stroke-width="1.6" stroke-dasharray="6,4"/>
  <line x1="{mx0}" y1="{mid_y:.1f}" x2="{mx0 + mw}" y2="{mid_y:.1f}" stroke="#475569" stroke-width="1.6" stroke-dasharray="6,4"/>
""")

    # Ticks
    for xt in [0.0, 0.25, 0.50, 0.75, 1.0]:
        gx, _ = map_cs(xt, 0)
        parts.append(f'<text x="{gx:.1f}" y="{my0 + mh + 20}" text-anchor="middle" font-family="{FONT_MONO}" font-size="10.5" fill="#334155">{xt:.2f}</text>')
    for yt in [0.0, 0.25, 0.50, 0.75, 0.86, 1.0]:
        _, gy = map_cs(0, yt)
        col = "#DC2626" if yt == 0.86 else "#334155"
        parts.append(f'<text x="{mx0 - 10}" y="{gy + 4:.1f}" text-anchor="end" font-family="{FONT_MONO}" font-size="10.5" font-weight="{"700" if yt == 0.86 else "400"}" fill="{col}">{yt:.2f}</text>')

    # Smooth Required Human Damping h_crit Contour Curves: 0.35*C + 0.65*S = level
    for h_lvl, c_col, lbl_c in [
        (0.28, "#059669", "h_crit = 0.15"),
        (0.50, "#0284C7", "h_crit = 0.45"),
        (0.72, "#7C3AED", "h_crit = 0.80"),
    ]:
        c_vals = np.linspace(0.0, 1.0, 100)
        pts = []
        for cv in c_vals:
            sv = (h_lvl - 0.34 * cv) / 0.66
            if 0.02 <= sv <= 0.85:
                pts.append(map_cs(cv, sv))
        if len(pts) > 2:
            pstr = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            parts.append(f'<polyline points="{pstr}" fill="none" stroke="{c_col}" stroke-width="1.8" stroke-dasharray="4,4"/>')

    # Forbidden Banner Text
    parts.append(f"""
  <text x="{mx0 + mw/2:.1f}" y="{my0 + 19}" text-anchor="middle" font-family="{FONT_MONO}" font-size="11.2" font-weight="800" fill="#991B1B">FORBIDDEN AUTONOMOUS ZONE (S_y.m ≥ 0.86) — AI SAFETY Z-LAW VETO (h = 1.00 MANDATORY)</text>
  <text x="{mx0 + mw/2:.1f}" y="{my0 + 36}" text-anchor="middle" font-family="{FONT_SANS}" font-size="10.4" fill="#7F1D1D">Zero algorithmic firing, punitive scoring, medical/legal coercion, or interpersonal manipulation (DCC prohibited)</text>
""")

    # Quadrant Titles (halo-stroked for crisp legibility over dashed contours)
    halo = 'paint-order="stroke" stroke="#FFFFFF" stroke-width="3.5" stroke-opacity="0.88" stroke-linejoin="round"'
    parts.append(f"""
  <text x="{mx0 + 16}" y="{mid_y + 24:.1f}" font-family="{FONT_MONO}" font-size="11" font-weight="800" fill="#065F46" {halo}>QUADRANT I • FULL AUTOMATION (h = 0)</text>
  <text x="{mx0 + 16}" y="{mid_y + 42:.1f}" font-family="{FONT_SANS}" font-size="10.6" fill="#1E293B" {halo}>Deterministic, idempotent, Z-safe tasks</text>

  <text x="{mid_x + 16:.1f}" y="{mid_y + 24:.1f}" font-family="{FONT_MONO}" font-size="11" font-weight="800" fill="#0369A1" {halo}>QUADRANT II • SHIELDED AI PIPELINE</text>
  <text x="{mid_x + 16:.1f}" y="{mid_y + 42:.1f}" font-family="{FONT_SANS}" font-size="10.6" fill="#1E293B" {halo}>EPCSIS = Z[N+1] + Δ-Exception Gate (0.15 ≤ h ≤ 0.45)</text>

  <text x="{mx0 + 16}" y="{my0 + forbid_h + 24:.1f}" font-family="{FONT_MONO}" font-size="11" font-weight="800" fill="#92400E" {halo}>QUADRANT III • CONSENT CO-PILOT</text>
  <text x="{mx0 + 16}" y="{my0 + forbid_h + 42:.1f}" font-family="{FONT_SANS}" font-size="10.6" fill="#1E293B" {halo}>AI drafts options; Human approves (0.45 &lt; h ≤ 0.80)</text>

  <text x="{mid_x + 16:.1f}" y="{my0 + forbid_h + 24:.1f}" font-family="{FONT_MONO}" font-size="11" font-weight="800" fill="#5B21B6" {halo}>QUADRANT IV • SOVEREIGN HUMAN CRAFT</text>
  <text x="{mid_x + 16:.1f}" y="{my0 + forbid_h + 42:.1f}" font-family="{FONT_SANS}" font-size="10.6" fill="#1E293B" {halo}>Meaning creation, ethics &amp; strategy (0.80 &lt; h ≤ 1.00)</text>
""")

    # Plotted Benchmark Processes (Enterprise Circles, Daily Life Diamonds)
    samples = [
        (0.15, 0.12, "E1: CI/CD &amp; Backups", "ent", "#059669", "right"),
        (0.24, 0.23, "L1: Bill Autopay &amp; Sync", "life", "#059669", "right"),
        (0.93, 0.16, "E2: Log Anomaly Triage", "ent", "#0284C7", "left"),
        (0.91, 0.30, "L2: Research RAG Digest", "life", "#0284C7", "left"),
        (0.18, 0.62, "E3: Customer Refund Appeal", "ent", "#D97706", "right"),
        (0.20, 0.73, "L3: Health &amp; Budget Plan", "life", "#D97706", "right"),
        (0.94, 0.59, "E4: Org Architecture &amp; Hiring", "ent", "#5B21B6", "left"),
        (0.94, 0.72, "L4: Core Relationships &amp; Vows", "life", "#5B21B6", "left"),
        (0.95, 0.892, "E5: Layoffs / Disciplinary Action", "ent", "#DC2626", "left"),
    ]
    for cx_v, sy_v, label_s, kind, col_s, side in samples:
        px, py = map_cs(cx_v, sy_v)
        if kind == "ent":
            parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6.5" fill="{col_s}" stroke="#FFFFFF" stroke-width="2"/>')
        else:
            parts.append(f'<polygon points="{px:.1f},{py-7.5:.1f} {px+7.5:.1f},{py:.1f} {px:.1f},{py+7.5:.1f} {px-7.5:.1f},{py:.1f}" fill="{col_s}" stroke="#FFFFFF" stroke-width="2"/>')
        pill_w = len(label_s.replace("&amp;", "&")) * 6.15 + 14.0
        rx_pill = (px + 11.0) if side == "right" else (px - pill_w - 11.0)
        parts.append(f'<rect x="{rx_pill:.1f}" y="{py - 10:.1f}" width="{pill_w:.1f}" height="20" rx="4" fill="#FFFFFF" fill-opacity="0.95" stroke="{col_s}" stroke-width="1.1"/>')
        parts.append(f'<text x="{rx_pill + 7:.1f}" y="{py + 4:.1f}" font-family="{FONT_SANS}" font-size="10.1" font-weight="600" fill="#0F172A">{label_s}</text>')

    # Axes Titles
    parts.append(f"""
  <text x="{mx0 + mw/2:.1f}" y="{my0 + mh + 46}" text-anchor="middle" font-family="{FONT_SANS}" font-size="12.5" font-weight="700" fill="#0F172A">Syntactic &amp; Operational Complexity C_x.n ∈ [0, 1]  (Deterministic Rules → Multi-Agent Stochasticity)</text>
  <g transform="translate(34, {my0 + mh/2:.1f}) rotate(-90)">
    <text x="0" y="0" text-anchor="middle" font-family="{FONT_SANS}" font-size="12.5" font-weight="700" fill="#0F172A">Human, Semantic &amp; Ethical Z-Sensitivity S_y.m ∈ [0, 1]</text>
  </g>
""")

    # Right Side Decision Guide Panel
    rx = 842
    parts.append(f"""
  <rect x="{rx}" y="{my0}" width="306" height="{mh}" rx="10" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.6" filter="url(#cardShadow)"/>
  <rect x="{rx}" y="{my0}" width="306" height="36" rx="9" fill="url(#navyGrad)"/>
  <text x="{rx + 153}" y="{my0 + 23}" text-anchor="middle" font-family="{FONT_MONO}" font-size="11.2" font-weight="700" fill="#FBBF24">SOVEREIGNTY EXECUTION RULES</text>

  <text x="{rx + 16}" y="{my0 + 60}" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#0F172A">STABILITY CONDITION:</text>
  <rect x="{rx + 16}" y="{my0 + 70}" width="274" height="46" rx="6" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1"/>
  <text x="{rx + 153}" y="{my0 + 90}" text-anchor="middle" font-family="{FONT_MONO}" font-size="11" font-weight="700" fill="#1E3A8A">ρ((1 − h)J_A + hJ_H) &lt; 1</text>
  <text x="{rx + 153}" y="{my0 + 107}" text-anchor="middle" font-family="{FONT_SANS}" font-size="10.2" fill="#475569">Human damping h prevents drift runaway</text>

  <text x="{rx + 16}" y="{my0 + 142}" font-family="{FONT_SANS}" font-size="11.5" font-weight="700" fill="#065F46">1. Automate Only x.n Mechanics</text>
  <text x="{rx + 16}" y="{my0 + 159}" font-family="{FONT_SANS}" font-size="10.6" fill="#334155">Never automate y.m meaning, empathy,</text>
  <text x="{rx + 16}" y="{my0 + 174}" font-family="{FONT_SANS}" font-size="10.6" fill="#334155">or moral accountability.</text>

  <text x="{rx + 16}" y="{my0 + 204}" font-family="{FONT_SANS}" font-size="11.5" font-weight="700" fill="#0369A1">2. Mandatory Reversibility</text>
  <text x="{rx + 16}" y="{my0 + 221}" font-family="{FONT_SANS}" font-size="10.6" fill="#334155">Every automated step must support</text>
  <text x="{rx + 16}" y="{my0 + 236}" font-family="{FONT_SANS}" font-size="10.6" fill="#334155">1-click human override &amp; rollback.</text>

  <text x="{rx + 16}" y="{my0 + 266}" font-family="{FONT_SANS}" font-size="11.5" font-weight="700" fill="#92400E">3. Decontaminate First ("Achtung")</text>
  <text x="{rx + 16}" y="{my0 + 283}" font-family="{FONT_SANS}" font-size="10.6" fill="#334155">Automating a coercive legacy process</text>
  <text x="{rx + 16}" y="{my0 + 298}" font-family="{FONT_SANS}" font-size="10.6" fill="#334155">multiplies Z-decay speed exponentially.</text>

  <text x="{rx + 16}" y="{my0 + 328}" font-family="{FONT_SANS}" font-size="11.5" font-weight="700" fill="#991B1B">4. AI Safety Z-Law Veto</text>
  <text x="{rx + 16}" y="{my0 + 345}" font-family="{FONT_SANS}" font-size="10.6" fill="#334155">If live telemetry detects σ_Z &gt; 1.15,</text>
  <text x="{rx + 16}" y="{my0 + 360}" font-family="{FONT_SANS}" font-size="10.6" fill="#334155">h jumps to 1.00 (immediate human</text>
  <text x="{rx + 16}" y="{my0 + 375}" font-family="{FONT_SANS}" font-size="10.6" fill="#334155">takeover).</text>

  <line x1="{rx + 16}" y1="{my0 + 398}" x2="{rx + 290}" y2="{my0 + 398}" stroke="#E2E8F0" stroke-width="1.5"/>
  <text x="{rx + 16}" y="{my0 + 420}" font-family="{FONT_MONO}" font-size="10.5" font-weight="700" fill="#0F172A">MARKER KEY:</text>
  <circle cx="{rx + 26}" cy="{my0 + 442}" r="6" fill="#0284C7"/>
  <text x="{rx + 40}" y="{my0 + 446}" font-family="{FONT_SANS}" font-size="11" fill="#334155">Enterprise Process (E1–E5)</text>
  <polygon points="{rx + 26},{my0 + 462} {rx + 33},{my0 + 469} {rx + 26},{my0 + 476} {rx + 19},{my0 + 469}" fill="#059669"/>
  <text x="{rx + 40}" y="{my0 + 473}" font-family="{FONT_SANS}" font-size="11" fill="#334155">Daily Life Process (L1–L4)</text>
""")

    parts.append("</svg>")
    save_and_validate_svg("fig6_automation_sovereignty_matrix.svg", "\n".join(parts))


if __name__ == "__main__":
    print("Generating CSI Process Design Blueprint Visual Assets...")
    build_fig1()
    build_fig2()
    build_fig3()
    build_fig4()
    build_fig5()
    build_fig6()
    print("All 6 precision SVG figures generated and XML-validated successfully.")
