#!/usr/bin/env python3
"""Render the Skill Atlas artwork (SVG -> PNG) with Poppins.

    python3 tools/render_assets.py          # writes assets/{banner,architecture,map}.{svg,png}

Everything is generated here so the artwork is reviewable as code, not a binary blob.
Glyph note: Poppins has no U+2192 (arrow) and no U+25B8 — both render as tofu. Use '›' and '·'.
"""
import os
import cairosvg

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
BG0, BG1 = "#070B14", "#04060C"
INK, MUTED, DIM = "#FFFFFF", "#B7C2D4", "#7A879E"
TEAL, VIOLET, AMBER = "#2BE3C4", "#8C7BFF", "#FFC46B"
STROKE = "#1B2436"

HEAD = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{bg0}"/><stop offset="1" stop-color="{bg1}"/>
  </linearGradient>
  <radialGradient id="glowA" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{teal}" stop-opacity="0.22"/>
    <stop offset="1" stop-color="{teal}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowB" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{violet}" stop-opacity="0.26"/>
    <stop offset="1" stop-color="{violet}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{teal}"/><stop offset="1" stop-color="{violet}"/>
  </linearGradient>
</defs>
<rect width="{w}" height="{h}" fill="url(#bg)"/>
"""


def grid(w, h, step=40, op=0.03):
    p = [f'<g stroke="#FFFFFF" stroke-opacity="{op}" stroke-width="1">']
    for x in range(step, w, step):
        p.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>')
    for y in range(step, h, step):
        p.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>')
    p.append("</g>")
    return "".join(p)


def t(x, y, s, size=24, fill=INK, weight=400, spacing=0, anchor="start", opacity=1.0, family="Poppins"):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" letter-spacing="{spacing}" text-anchor="{anchor}" opacity="{opacity}">{s}</text>')


def pill(x, y, label, w, h=34, fill="#0E1526", stroke=STROKE, color=MUTED, size=13, spacing=1.6):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{stroke}"/>'
            + t(x + w / 2, y + h / 2 + size * 0.36, label, size=size, fill=color, weight=500,
                spacing=spacing, anchor="middle"))


# ---------------------------------------------------------------- banner
def banner():
    w, h = 1280, 640
    s = [HEAD.format(w=w, h=h, bg0=BG0, bg1=BG1, teal=TEAL, violet=VIOLET)]
    s.append('<ellipse cx="1080" cy="120" rx="520" ry="420" fill="url(#glowB)"/>')
    s.append('<ellipse cx="120" cy="560" rx="520" ry="380" fill="url(#glowA)"/>')
    s.append(grid(w, h))
    s.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{STROKE}"/>')

    s.append('<rect x="84" y="86" width="46" height="2" fill="url(#accent)"/>')
    s.append(t(144, 92, "AGENT SKILLS  —  OPEN SOURCE", 14, TEAL, 500, spacing=4))

    s.append(t(84, 208, "SKILL", 104, INK, 700, spacing=-2))
    s.append(t(84, 304, "ATLAS", 104, "url(#accent)", 700, spacing=-2))
    s.append(t(86, 364, "Forty production-grade skills for coding agents.", 25, MUTED, 400))
    s.append(t(86, 404, 'Plan <tspan fill="%s">›</tspan> test <tspan fill="%s">›</tspan> review '
                        '<tspan fill="%s">›</tspan> verify' % (TEAL, TEAL, TEAL), 25, INK, 500))

    for label, cw, x in (("40 SKILLS", 148, 84), ("5 RULES", 118, 244), ("MIT", 74, 374)):
        s.append(pill(x, 448, label, cw))
    s.append(t(86, 522, "Runs on  Claude Code · Codex · Cursor · Hermes", 16, TEAL, 500, spacing=0.4))

    layers = [("SKILLS", "workflow bodies", TEAL), ("AGENTS", "scoped personas", VIOLET),
              ("RULES", "always on", MUTED), ("HOOKS", "deterministic gates", AMBER)]
    bx, by, bw, bh, gap = 812, 176, 372, 66, 16
    for i, (name, note, color) in enumerate(layers):
        y = by + i * (bh + gap)
        s.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{bh}" rx="12" fill="{color}" fill-opacity="0.10" '
                 f'stroke="{color}" stroke-opacity="0.45"/>')
        s.append(f'<rect x="{bx}" y="{y}" width="4" height="{bh}" rx="2" fill="{color}"/>')
        s.append(t(bx + 26, y + 29, name, 17, INK, 600, spacing=2.4))
        s.append(t(bx + 26, y + 51, note, 14, MUTED))
        s.append(t(bx + bw - 22, y + 40, f"0{i+1}", 15, color, 600, anchor="end", opacity=0.85))

    s.append(t(84, 566, "curated from affaan-m/ECC (MIT)", 15, MUTED))
    s.append(t(bx + bw, 566, "github.com/ahmadvahidi/skill-atlas", 15, MUTED, 500, anchor="end"))
    s.append("</svg>")
    return "".join(s)


# ---------------------------------------------------------------- architecture
def architecture():
    w, h = 1600, 900
    s = [HEAD.format(w=w, h=h, bg0=BG0, bg1=BG1, teal=TEAL, violet=VIOLET)]
    s.append(grid(w, h))
    s.append('<ellipse cx="1380" cy="120" rx="420" ry="320" fill="url(#glowB)"/>')
    s.append(t(80, 92, "THE HARNESS", 34, INK, 700, spacing=1))
    s.append(t(80, 130, "Five layers, one loop: nothing here runs on its own — the harness reads the markdown.",
               18, MUTED))

    s.append(t(80, 166, "HARNESS LAYERS", 13, DIM, 600, spacing=3.2))
    rows = [
        ("01", "SKILLS", "canonical workflow bodies, loaded on demand", TEAL),
        ("02", "AGENTS", "scoped persona + tool permissions, one job each", VIOLET),
        ("03", "COMMANDS", "slash shims — legacy surface, logic lives in skills", DIM),
        ("04", "RULES", "always-on constraints: immutability, coverage, secrets", MUTED),
        ("05", "HOOKS", "PreToolUse · PostToolUse · Stop · PreCompact", AMBER),
    ]
    x, y0, bw, bh, gap = 80, 190, 720, 100, 22
    for i, (num, name, note, color) in enumerate(rows):
        y = y0 + i * (bh + gap)
        s.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="14" fill="#0B1220" stroke="{STROKE}"/>')
        s.append(f'<rect x="{x}" y="{y}" width="5" height="{bh}" rx="3" fill="{color}" opacity="0.9"/>')
        s.append(t(x + 28, y + 40, num, 15, color, 600, spacing=2))
        s.append(t(x + 74, y + 42, name, 22, INK, 600, spacing=1.6))
        s.append(t(x + 74, y + 72, note, 15, MUTED))
        s.append(f'<circle cx="{x+bw-34}" cy="{y+bh/2}" r="7" fill="{color}" opacity="0.75"/>')

    px, py, pw = 900, 176, 620
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="590" rx="18" fill="#0A111F" stroke="{STROKE}"/>')
    s.append(t(px + 92, py + 48, "THE PHASE PIPELINE", 17, INK, 600, spacing=2.6))
    s.append(t(px + 92, py + 74, "one input, one output per phase — never skip, never merge", 14, MUTED))
    steps = [("RESEARCH", "what is true today"), ("PLAN", "phases, risks, files"),
             ("IMPLEMENT (TDD)", "red › green › refactor"), ("REVIEW", "different pass than the writer"),
             ("VERIFY", "gates that actually ran"), ("COMMIT", "conventional, scoped")]
    sy = py + 116
    for i, (step, note) in enumerate(steps):
        cy = sy + i * 74
        col = TEAL if i < 3 else (AMBER if i == 4 else VIOLET)
        if i < len(steps) - 1:
            s.append(f'<line x1="{px+58}" y1="{cy+22}" x2="{px+58}" y2="{cy+74}" stroke="{STROKE}" stroke-width="2"/>')
        s.append(f'<circle cx="{px+58}" cy="{cy+14}" r="15" fill="#0E1526" stroke="{col}" stroke-width="2"/>')
        s.append(t(px + 58, cy + 19, str(i + 1), 13, col, 600, anchor="middle"))
        s.append(t(px + 92, cy + 20, step, 19, INK, 500, spacing=1.2))
        s.append(t(px + 92, cy + 42, note, 14, MUTED))

    # the loop: a failed gate returns to implement, not to plan
    rx = px + pw - 46
    top = sy + 2 * 74 + 14        # IMPLEMENT node
    bottom = sy + 5 * 74 + 14     # COMMIT node
    s.append(f'<path d="M{rx} {bottom} L{rx} {top}" stroke="{AMBER}" stroke-opacity="0.55" '
             f'stroke-width="2" stroke-dasharray="5 6" fill="none"/>')
    s.append(f'<path d="M{rx-6} {top+12} L{rx} {top} L{rx+6} {top+12}" stroke="{AMBER}" stroke-opacity="0.8" '
             f'stroke-width="2" fill="none"/>')
    s.append(f'<rect x="{rx-108}" y="{top+26}" width="216" height="64" rx="8" fill="#0E1526" stroke="{AMBER}" '
             f'stroke-opacity="0.35"/>')
    s.append(t(rx, top + 50, "gate fails", 14, AMBER, 600, anchor="middle"))
    s.append(t(rx, top + 72, "back to implement", 13, MUTED, anchor="middle"))

    s.append(f'<rect x="80" y="800" width="1440" height="60" rx="12" fill="#0B1220" stroke="{STROKE}"/>')
    s.append(t(104, 837, "MEMORY", 15, TEAL, 600, spacing=2.4))
    s.append(t(202, 837, "worked  /  failed  /  not attempted   —   saved by the PreCompact + Stop hooks, "
                         "reloaded by SessionStart", 15, MUTED))
    s.append(t(w - 80, 837, "affaan-m/ECC › skill-atlas", 14, DIM, anchor="end"))
    s.append("</svg>")
    return "".join(s)


# ---------------------------------------------------------------- map
GROUPS = [
    ("WORKFLOW", TEAL, ["tdd-workflow", "verification-loop", "plan-orchestrate", "orch-pipeline",
                        "brownfield-retrospective", "codebase-onboarding", "continuous-learning",
                        "context-budget", "coding-standards", "api-design", "conventional-commit-review",
                        "unified-memory", "security-review"]),
    ("AGENTS + AI", VIOLET, ["agent-architecture-audit", "agent-eval", "agent-harness-construction",
                             "agent-introspection-debugging", "agent-security-hardening",
                             "agent-self-evaluation", "iterative-retrieval", "prompt-optimizer"]),
    ("BACKEND + DATA", AMBER, ["postgres-patterns", "database-migrations", "redis-patterns",
                               "error-handling", "backend-patterns", "fastapi-patterns"]),
    ("LANGUAGES + RUNTIME", TEAL, ["python-testing", "golang-testing", "rust-testing", "react-testing",
                                   "docker-patterns", "kubernetes-patterns"]),
    ("FRONTEND + DESIGN", VIOLET, ["frontend-patterns", "design-system", "accessibility",
                                   "react-performance"]),
    ("PRODUCT + CONTENT", AMBER, ["seo", "market-research", "content-engine"]),
]


def map_svg():
    total = sum(len(g[2]) for g in GROUPS)
    w, h = 1600, 1030
    s = [HEAD.format(w=w, h=h, bg0=BG0, bg1=BG1, teal=TEAL, violet=VIOLET)]
    s.append(grid(w, h))
    s.append(t(80, 92, "WHAT IS INSIDE", 34, INK, 700, spacing=1))
    s.append(t(80, 130, f"All {total} skills, by group. The full 314-skill catalogue is in docs/catalog.md.",
               18, MUTED))

    cw, ch, gx, gy = 708, 246, 24, 20
    for i, (name, color, skills) in enumerate(GROUPS):
        cx = 80 + (i % 2) * (cw + gx)
        cy = 176 + (i // 2) * (ch + gy)
        s.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="16" fill="#0A111F" stroke="{STROKE}"/>')
        s.append(f'<rect x="{cx}" y="{cy}" width="150" height="3" rx="2" fill="{color}" opacity="0.85"/>')
        s.append(t(cx + 28, cy + 50, name, 19, INK, 600, spacing=2.2))
        s.append(t(cx + cw - 28, cy + 52, str(len(skills)), 28, color, 700, anchor="end"))
        colw = (cw - 56 - 16) / 3
        for j, skill in enumerate(skills):
            col, row = divmod(j, 5)
            sx = cx + 28 + col * (colw + 8)
            sy = cy + 78 + row * 33
            s.append(f'<rect x="{sx}" y="{sy}" width="{colw-6}" height="27" rx="7" fill="#0E1526" stroke="{STROKE}"/>')
            s.append(f'<circle cx="{sx+15}" cy="{sy+13.5}" r="2.6" fill="{color}" opacity="0.85"/>')
            size = 12.5 if len(skill) <= 20 else (11.4 if len(skill) <= 24 else 10.6)
            s.append(t(sx + 24, sy + 18.5, skill, size, MUTED))
    s.append(t(80, 1000, "MIT · derived from affaan-m/ECC · every file keeps its upstream attribution",
               14, DIM))
    s.append("</svg>")
    return "".join(s)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, svg in (("banner", banner()), ("architecture", architecture()), ("map", map_svg())):
        open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(svg)
        png = os.path.join(OUT, name + ".png")
        cairosvg.svg2png(bytestring=svg.encode(), write_to=png, scale=2)
        print(name, os.path.getsize(png), "bytes")
