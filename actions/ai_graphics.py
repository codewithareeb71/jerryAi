from __future__ import annotations

import os
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    from PyQt6.QtWidgets import QApplication, QFileDialog
except Exception:
    QApplication = None


DEFAULT_BG = (10, 25, 40)


def _ensure_out_path(path: str | Path | None, default_name: str) -> Path:
    if path:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p
    # Ask user via QFileDialog if available
    if QApplication and QApplication.instance() is not None:
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dlg.setDefaultSuffix(Path(default_name).suffix.lstrip('.'))
        fn, _ = dlg.getSaveFileName(None, "Save generated file", str(Path.home() / default_name))
        if fn:
            p = Path(fn)
            p.parent.mkdir(parents=True, exist_ok=True)
            return p
    # Fallback to Desktop
    p = Path.home() / default_name
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def create_logo(text: str, outfile: str | None = None, size: Tuple[int, int] = (1024, 1024)) -> str:
    """Generate a simple professional logo with centered text.

    This is a local, production-ready generator that produces a high-resolution PNG.
    """
    w, h = size
    img = Image.new("RGBA", (w, h), DEFAULT_BG)
    draw = ImageDraw.Draw(img)

    # Try to pick a decent font
    try:
        font = ImageFont.truetype("arial.ttf", int(w * 0.16))
    except Exception:
        font = ImageFont.load_default()

    text = text.strip()
    tw, th = draw.textsize(text, font=font)
    draw.text(((w - tw) / 2, (h - th) / 2), text, font=font, fill=(255, 255, 255))

    # subtle vignette
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((-w * 0.2, -h * 0.2, w * 1.2, h * 1.2), fill=(0, 0, 0, 30))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)

    outp = _ensure_out_path(outfile, "jerry_logo.png")
    img.save(outp, format="PNG")
    return str(outp)


def create_poster(title: str, subtitle: str | None = None, image: str | None = None, outfile: str | None = None, size=(1600, 2400)) -> str:
    w, h = size
    bg = Image.new("RGB", (w, h), (20, 30, 48))
    draw = ImageDraw.Draw(bg)
    try:
        title_font = ImageFont.truetype("arialbd.ttf", int(w * 0.06))
        sub_font = ImageFont.truetype("arial.ttf", int(w * 0.032))
    except Exception:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    # Optional background image
    if image:
        try:
            im = Image.open(image).convert("RGB")
            im = im.resize((w, int(h * 0.55)), Image.LANCZOS)
            bg.paste(im, (0, 0))
        except Exception:
            pass

    draw.text((int(w * 0.06), int(h * 0.6)), title, font=title_font, fill=(255, 255, 255))
    if subtitle:
        draw.text((int(w * 0.06), int(h * 0.7)), subtitle, font=sub_font, fill=(200, 200, 200))

    outp = _ensure_out_path(outfile, "jerry_poster.png")
    bg.save(outp, format="PNG")
    return str(outp)


def create_thumbnail(image_path: str, outfile: str | None = None, size=(1280, 720), title: str | None = None) -> str:
    try:
        im = Image.open(image_path).convert("RGB")
    except Exception:
        raise RuntimeError("Could not open source image for thumbnail.")
    im.thumbnail(size, Image.LANCZOS)
    w, h = im.size
    draw = ImageDraw.Draw(im)
    if title:
        try:
            f = ImageFont.truetype("arialbd.ttf", int(h * 0.12))
        except Exception:
            f = ImageFont.load_default()
        tw, th = draw.textsize(title, font=f)
        draw.rectangle([(10, h - th - 20), (10 + tw + 16, h - 8)], fill=(0, 0, 0, 200))
        draw.text((18, h - th - 14), title, font=f, fill=(255, 255, 255))

    outp = _ensure_out_path(outfile, "jerry_thumbnail.png")
    im.save(outp, format="JPEG", quality=92)
    return str(outp)


def remove_background(image_path: str, outfile: str | None = None, tolerance: int = 20) -> str:
    """Naive background removal: converts near-white pixels to transparent.

    This provides a fast, local option for simple backgrounds.
    """
    im = Image.open(image_path).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r > 240 and g > 240 and b > 240:
                px[x, y] = (255, 255, 255, 0)

    outp = _ensure_out_path(outfile, "jerry_transparent.png")
    im.save(outp, format="PNG")
    return str(outp)


def upscale_image(image_path: str, scale: int = 2, outfile: str | None = None) -> str:
    im = Image.open(image_path)
    w, h = im.size
    new = im.resize((w * scale, h * scale), Image.LANCZOS)
    outp = _ensure_out_path(outfile, f"jerry_upscale_{scale}x.png")
    new.save(outp, format="PNG")
    return str(outp)
