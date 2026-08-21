#!/usr/bin/env python3
"""Convertit une image en art ASCII pour le README de profil GitHub."""
import sys
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

# Ramp 70 niveaux : du plus sombre (@) au plus clair (espace)
RAMP = "@%#WMoahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def to_ascii(path, width=52, n_lines=28, crop=None, contrast=2.2, invert=False):
    img = Image.open(path)
    if invert:
        img = ImageOps.invert(img.convert("RGB"))

    if crop:
        w, h = img.size
        l, t, r, b = crop
        img = img.crop((int(l * w), int(t * h), int(r * w), int(b * h)))

    # Amplification de la couronne dorée vs fond gris via R-B channel trick
    r_ch, g_ch, b_ch = img.split()
    arr_r = np.array(r_ch, dtype=float)
    arr_b = np.array(b_ch, dtype=float)
    arr = arr_r * 0.7 + (arr_r - arr_b) * 0.5
    arr = np.clip(arr, 0, 255)

    img = Image.fromarray(arr.astype(np.uint8))
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
    img = img.resize((width, n_lines), Image.LANCZOS)

    px = img.load()
    n = len(RAMP) - 1
    lines = []
    for y in range(n_lines):
        row = [RAMP[int(px[x, y] / 255 * n)] for x in range(width)]
        lines.append("".join(row))
    return lines

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "Gemini_Generated_Image_etck1etck1etck1e.jpg"
    crop = (0.28, 0.0, 0.72, 0.53)
    for line in to_ascii(path, crop=crop, invert="--inv" in sys.argv):
        print(line)
