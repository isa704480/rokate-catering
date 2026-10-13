"""Model maydonlaridan frontend forma uchun sxema va qiymatlar yasash."""
from datetime import date, datetime
from decimal import Decimal

from django.db import models
from django.utils import timezone
from modeltranslation.translator import NotRegistered, translator

from apps.core.images import image_data

LANGS = ("en", "ru")
SEO_NAMES = {"seo_title", "seo_description", "og_image", "noindex"}

VIRTUAL = {
    "source": ("Источник", lambda o: o.source_label),
    "items_count": ("Позиций", lambda o: o.items.count()),
    "photos": ("Фото", lambda o: o.images.count()),
}


def translated_fields(model):
    try:
        return set(translator.get_options_for_model(model).all_fields.keys())
    except NotRegistered:
        return set()


def field_type(f):
    if f.choices:
        return "select"
    if isinstance(f, models.ImageField):
        return "image"
    if isinstance(f, models.FileField):
        return "file"
    if isinstance(f, models.ForeignKey):
        return "fk"
    if isinstance(f, models.ManyToManyField):
        return "m2m"
    if isinstance(f, models.BooleanField):
        return "bool"
    if isinstance(f, models.DateTimeField):
        return "datetime"
    if isinstance(f, models.DateField):
        return "date"
    if isinstance(f, (models.IntegerField, models.DecimalField)):
        return "number"
    if isinstance(f, models.SlugField):
        return "slug"
    if isinstance(f, models.EmailField):
        return "email"
    if isinstance(f, models.URLField):
        return "url"
    if isinstance(f, models.TextField):
        return "textarea"
    return "text"


def related_options(f):
    qs = f.related_model.objects.all()
    return [{"value": o.pk, "label": str(o)} for o in qs]


def field_def(model, name, readonly=False):
    if name in VIRTUAL:
        return {"name": name, "label": VIRTUAL[name][0], "type": "text", "translated": False, "readonly": True}
    tr = name in translated_fields(model)
    f = model._meta.get_field(name)
    ftype = field_type(f)
    actual = model._meta.get_field(f"{name}_en") if tr else f
    d = {
        "name": name,
        "label": (lambda s: s[:1].upper() + s[1:])(str(f.verbose_name)),
        "type": ftype,
        "translated": tr,
        "required": not actual.blank and ftype not in ("bool",) and not readonly,
        "help": str(f.help_text or ""),
        "readonly": readonly,
        "seo": name in SEO_NAMES,
    }
    if getattr(f, "max_length", None) and ftype in ("text", "slug", "email", "url"):
        d["max_length"] = f.max_length
    if ftype == "select":
        d["options"] = [{"value": v, "label": str(lbl)} for v, lbl in f.choices]
    if ftype in ("fk", "m2m"):
        d["options"] = related_options(f)
    if ftype == "number" and isinstance(f, models.DecimalField):
        d["step"] = "any"
    return d


def file_value(ff):
    if not ff:
        return None
    data = {"url": ff.url, "name": ff.name.rsplit("/", 1)[-1]}
    if isinstance(ff.field, models.ImageField):
        img = image_data(ff)
        if img:
            data["thumb"] = img["srcset"].split(", ")[0].split(" ")[0] if img["srcset"] else img["src"]
    return data


def plain(v):
    if isinstance(v, datetime):
        return timezone.localtime(v).strftime("%Y-%m-%d %H:%M") if timezone.is_aware(v) else v.strftime("%Y-%m-%d %H:%M")
    if isinstance(v, date):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v) if v % 1 else int(v)
    return v


def field_value(obj, name):
    """Formaga beriladigan qiymat (tarjimali bo'lsa {'en':..,'ru':..})."""
    model = type(obj)
    if name in VIRTUAL:
        return VIRTUAL[name][1](obj)
    if name in translated_fields(model):
        return {lang: getattr(obj, f"{name}_{lang}") or "" for lang in LANGS}
    f = model._meta.get_field(name)
    t = field_type(f)
    if t in ("image", "file"):
        return file_value(getattr(obj, name))
    if t == "fk":
        return getattr(obj, f"{name}_id")
    if t == "m2m":
        return list(getattr(obj, name).values_list("pk", flat=True)) if obj.pk else []
    return plain(getattr(obj, name))


def display_value(obj, name):
    """Ro'yxat (jadval) uchun ko'rinish."""
    model = type(obj)
    if name in VIRTUAL:
        return VIRTUAL[name][1](obj)
    f = model._meta.get_field(name)
    t = field_type(f)
    if t == "image":
        v = file_value(getattr(obj, name))
        return {"thumb": v.get("thumb") or v["url"]} if v else None
    if t == "select":
        return {"value": getattr(obj, name), "label": getattr(obj, f"get_{name}_display")()}
    if t == "fk":
        rel = getattr(obj, name)
        return str(rel) if rel else ""
    if t == "bool":
        return bool(getattr(obj, name))
    return plain(getattr(obj, name))


def form_field_names(model, names):
    """Saqlash uchun haqiqiy model maydonlari (tarjimalilar _en/_ru ga kengaytiriladi)."""
    tr = translated_fields(model)
    out = []
    for n in names:
        if n.startswith("@") or n in VIRTUAL:
            continue
        if n in tr:
            out += [f"{n}_{lang}" for lang in LANGS]
        else:
            out.append(n)
    return out
