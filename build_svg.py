#!/usr/bin/env python3
"""
Génère un SVG style terminal : ASCII art à gauche + bloc info à droite.
Usage : python3 build_svg.py  →  terminal.svg
"""
import html, re

# ── Paramètres de rendu ──────────────────────────────────────────────────────
FONT        = "Courier New, Courier, monospace"
ART_FS      = 2.82     # font-size pour l'art (px) — réduit pour aligner la hauteur sur le bloc info
ART_CW      = 1.69     # largeur d'un caractère (px) – Courier New ≈ 0.6×font
ART_LH      = 3.38     # hauteur d'une ligne (px)  — 68 lignes × 3.38 ≈ 230px = 20 × 11.5

INFO_FS     = 9        # font-size pour le bloc info
INFO_CW     = 5.4      # 0.6 × 9
INFO_LH     = 11.5

PAD         = 14       # marge intérieure
GAP         = 18       # espace entre l'art et l'info
CHROME_H    = 22       # hauteur de la barre de titre terminal

# ── Couleurs ─────────────────────────────────────────────────────────────────
BG          = "#0d1117"   # fond fenêtre
CHROME_BG   = "#161b22"   # barre titre
ART_COL     = "#3fb950"   # vert GitHub contributions
HEADER_COL  = "#e6edf3"   # blanc cassé  (toi@github, tirets)
LABEL_COL   = "#79c0ff"   # bleu clair   (.OS:  ...)
VALUE_COL   = "#c9d1d9"   # gris clair   (valeurs)
SECTION_COL = "#ffa657"   # orange       (- Contact ---)

# ── Info bloc (à remplir) ────────────────────────────────────────────────────
INFO = [
    ("header",  "4dm1nistrateur@github  ──────────────────────"),
    ("label",   ".OS:          ..................  MacOS, Windows 11"),
    ("label",   ".Uptime:      ................  26 years"),
    ("label",   ".Host:        ............  GIE Convergence"),
    ("label",   ".Editeur:     ...........  VSCode"),
    ("empty",   ""),
    ("label",   ".Langages.Prog:  .......  Python, Javascript"),
    ("label",   ".Langages.Web:   .....  HTML, CSS"),
    ("label",   ".Langages.Parles: ..  French, English"),
    ("empty",   ""),
    ("label",   ".Hobbies.Soft:  .....  All"),
    ("label",   ".Hobbies.Hard:  .....  All"),
    ("empty",   ""),
    ("section", "─ Contact ─────────────────────────────────"),
    ("label",   ".Email:  .....  mduterte@gie-convergence.fr"),
    ("empty",   ""),
    ("section", "─ GitHub Stats ─────────────────────────────"),
    ("label",   ".Repos:     ......................  3"),
]

COLOR_MAP = {
    "header":  HEADER_COL,
    "label":   LABEL_COL,
    "value":   VALUE_COL,
    "section": SECTION_COL,
    "empty":   ART_COL,
}

def color_info_line(kind, text):
    """Retourne du SVG pour une ligne d'info, avec coloration label/valeur."""
    if kind in ("empty", "header", "section"):
        col = COLOR_MAP[kind]
        return f'<tspan fill="{col}">{html.escape(text)}</tspan>'
    # kind == "label" : colorier le label (avant  "..") et la valeur séparément
    m = re.match(r'^(\.\S+\s+)(\.*\s*)(.*)', text)
    if m:
        label, dots, value = m.group(1), m.group(2), m.group(3)
        return (f'<tspan fill="{LABEL_COL}">{html.escape(label)}</tspan>'
                f'<tspan fill="{VALUE_COL}">{html.escape(dots)}</tspan>'
                f'<tspan fill="{VALUE_COL}">{html.escape(value)}</tspan>')
    return f'<tspan fill="{LABEL_COL}">{html.escape(text)}</tspan>'

def build_svg():
    # ── Charger l'art ────────────────────────────────────────────────────────
    with open("ASCII.txt") as f:
        art = [line.rstrip("\n") for line in f]
    art_cols = max(len(l) for l in art)
    art_rows = len(art)

    art_w = art_cols * ART_CW
    art_h = art_rows * ART_LH

    info_w = max(len(t) for _, t in INFO) * INFO_CW
    info_h = len(INFO) * INFO_LH

    total_w  = PAD + art_w + GAP + info_w + PAD
    total_h  = CHROME_H + PAD + max(art_h, info_h) + PAD

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{total_w:.0f}" height="{total_h:.0f}" '
        f'viewBox="0 0 {total_w:.0f} {total_h:.0f}">',

        # ── Fond principal ───────────────────────────────────────────────────
        f'<rect width="{total_w:.0f}" height="{total_h:.0f}" rx="8" fill="{BG}"/>',

        # ── Barre de titre ───────────────────────────────────────────────────
        f'<rect width="{total_w:.0f}" height="{CHROME_H}" rx="8" fill="{CHROME_BG}"/>',
        f'<rect y="12" width="{total_w:.0f}" height="10" fill="{CHROME_BG}"/>',
        # Boutons macOS-style
        f'<circle cx="14" cy="{CHROME_H/2:.0f}" r="5" fill="#ff5f56"/>',
        f'<circle cx="29" cy="{CHROME_H/2:.0f}" r="5" fill="#ffbd2e"/>',
        f'<circle cx="44" cy="{CHROME_H/2:.0f}" r="5" fill="#27c93f"/>',
        # Titre
        f'<text x="{total_w/2:.0f}" y="15" '
        f'font-family="{FONT}" font-size="9" fill="{HEADER_COL}" '
        f'text-anchor="middle">4dm1nistrateur@github: ~</text>',

        # ── Art ASCII ────────────────────────────────────────────────────────
        f'<g font-family="{FONT}" font-size="{ART_FS}" fill="{ART_COL}" '
        f'xml:space="preserve">',
    ]

    for i, row in enumerate(art):
        y = CHROME_H + PAD + (i + 1) * ART_LH
        lines.append(
            f'<text x="{PAD}" y="{y:.1f}">{html.escape(row)}</text>'
        )
    lines.append("</g>")

    # ── Bloc info ─────────────────────────────────────────────────────────────
    info_x = PAD + art_w + GAP
    lines.append(f'<g font-family="{FONT}" font-size="{INFO_FS}">')
    for i, (kind, text) in enumerate(INFO):
        y = CHROME_H + PAD + (i + 1) * INFO_LH
        inner = color_info_line(kind, text)
        lines.append(f'<text x="{info_x:.0f}" y="{y:.1f}">{inner}</text>')
    lines.append("</g>")

    lines.append("</svg>")
    return "\n".join(lines)

if __name__ == "__main__":
    svg = build_svg()
    with open("terminal.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("✓ terminal.svg généré")
