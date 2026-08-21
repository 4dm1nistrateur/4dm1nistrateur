#!/usr/bin/env python3
"""Assemble le README de profil : portrait ASCII a gauche + infos a droite."""
from img2ascii import to_ascii

PHOTO   = "Gemini_Generated_Image_etck1etck1etck1e.jpg"
CROP    = (0.28, 0.0, 0.72, 0.53)   # couronne + masque, sans les epaules
WIDTH   = 52
N_LINES = 28
GAP     = "   "

# ---- Bloc d'infos facon "neofetch" (a remplir) --------------------------
info = [
    "4dm1nistrateur@github  -------------------------------",
    ".OS: ................. MacOS, Windows 11",
    ".Uptime: ............. 26 years",
    ".Host: ............... GIE Convergence",
    ".Editeur: ............ VSCode",
    "",
    ".Langages.Prog: ...... Python, Javascript",
    ".Langages.Web: ....... HTML, CSS",
    ".Langages.Parles: .... French, English",
    "",
    ".Hobbies.Soft: ....... All",
    ".Hobbies.Hardware: ... All",
    "",
    "- Contact ----------------------------------",
    ".Email: .............. mduterte@gie-convergence.fr",
    ".LinkedIn: ........... X",
    "",
    "- GitHub Stats -----------------------------",
    ".Repos: .............. 3",
    ".Commits: ............ X",
    ".Followers: .......... X",
]

def main():
    art = to_ascii(PHOTO, width=WIDTH, n_lines=N_LINES, crop=CROP)
    n = max(len(art), len(info))
    lines = []
    for i in range(n):
        left  = art[i]  if i < len(art)  else " " * WIDTH
        right = info[i] if i < len(info) else ""
        lines.append((left.ljust(WIDTH) + GAP + right).rstrip())

    body = "```\n" + "\n".join(lines) + "\n```\n"

    readme = (
        "### Salut, moi c'est 4dm1nistrateur, jeune vibe codeur utilisant VSCode x Claud Code, road to the future. 🚀 \n\n"
        + body
        + "\n"
        "<!-- Astuce : ce README s'affiche sur ton profil si le depot\n"
        "     porte EXACTEMENT le meme nom que ton pseudo GitHub. -->\n"
    )

    with open("README.md", "w") as f:
        f.write(readme)
    print(readme)

if __name__ == "__main__":
    main()
