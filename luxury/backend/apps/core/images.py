"""Rasmlar uchun WebP variantlar (480/960/1600/2400 px).

Variantlar birinchi so'rovda yaratiladi va asl fayl yonida saqlanadi:
    portfolio/IMG_0897.jpg  ->  portfolio/IMG_0897__w960.webp
Asl fayl saytda ishlatilmaydi. EXIF (GPS va h.k.) variantlarga o'tmaydi.
"""
import base64
import io
import logging
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageOps

log = logging.getLogger(__name__)

WIDTHS = (480, 960, 1600, 2400)
QUALITY = 78


def _variant_name(name, width):
    base, _ = os.path.splitext(name)
    return f"{base}__w{width}.webp"


def _widths(w):
    """Asl kenglikka mos variant kengliklari: 480, 960, 1600, 2400 dan kichiklari + asl kenglik."""
    top = min(w, WIDTHS[-1])
    out = [x for x in WIDTHS if x < top]
    out.append(top)
    return out


def _meta_name(name):
    base, _ = os.path.splitext(name)
    return f"{base}__meta.txt"


def _ensure_variants(name):
    """Variantlarni yaratadi (agar yo'q bo'lsa) va (width, height, blur) qaytaradi."""
    meta_name = _meta_name(name)
    if default_storage.exists(meta_name):
        try:
            with default_storage.open(meta_name) as fh:
                w, h, blur = fh.read().decode().split("|", 2)
                return int(w), int(h), blur
        except Exception:  # noqa: BLE001
            pass

    with default_storage.open(name) as fh:
        img = Image.open(fh)
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGB")
    w, h = img.size

    for width in _widths(w):
        vname = _variant_name(name, width)
        if default_storage.exists(vname):
            continue
        copy = img.copy()
        copy.thumbnail((width, width * 4), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        copy.save(buf, "WEBP", quality=QUALITY, method=5)
        default_storage.save(vname, ContentFile(buf.getvalue()))

    tiny = img.copy()
    tiny.thumbnail((16, 16))
    buf = io.BytesIO()
    tiny.save(buf, "WEBP", quality=40)
    blur = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    default_storage.save(meta_name, ContentFile(f"{w}|{h}|{blur}".encode()))
    return w, h, blur


def image_data(field, alt=""):
    """API uchun rasm obyekti: {src, srcset, width, height, alt, blur} yoki None."""
    if not field:
        return None
    name = field.name
    try:
        w, h, blur = _ensure_variants(name)
    except Exception as exc:  # noqa: BLE001
        log.warning("Image variants failed for %s: %s", name, exc)
        return {"src": field.url, "srcset": "", "width": None, "height": None, "alt": alt, "blur": ""}

    widths = _widths(w)
    srcset = ", ".join(f"{default_storage.url(_variant_name(name, x))} {x}w" for x in widths)
    src = default_storage.url(_variant_name(name, widths[min(1, len(widths) - 1)]))
    return {"src": src, "srcset": srcset, "width": w, "height": h, "alt": alt, "blur": blur}


def file_url(field):
    return field.url if field else None
