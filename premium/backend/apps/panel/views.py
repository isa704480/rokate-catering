"""Frontend admin (/admin) uchun JSON API.

Autentifikatsiya: Django sessiyasi (httpOnly cookie) + CSRF token.
Faqat is_staff foydalanuvchilar. Har bir amal Django huquqlari bilan tekshiriladi
(superuser — hammasi; Roman uchun "Owner" guruhi, menejer uchun "Manager" guruhi).
"""
import csv
import json
from datetime import timedelta
from functools import wraps

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.forms import modelform_factory
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from apps.catering.models import CateringPackage, SeasonalOffer
from apps.leads.models import Inquiry, PartnerRequest
from apps.portfolio.models import PortfolioProject

from .registry import GROUPS, RESOURCES
from .schema import display_value, field_def, field_value, form_field_names, plain

PAGE_SIZE = 50


# ---------------------------------------------------------------- helpers

def err(msg, status=400, **extra):
    return JsonResponse({"ok": False, "error": msg, **extra}, status=status)


def can(user, model, action):
    if user.is_superuser:
        return True
    return user.has_perm(f"{model._meta.app_label}.{action}_{model._meta.model_name}")


def staff_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_staff and request.user.is_active):
            return err("auth", 401)
        return view(request, *args, **kwargs)
    return wrapped


def get_resource(key):
    res = RESOURCES.get(key)
    if not res:
        return None
    res.setdefault("key", key)
    return res


def body_json(request):
    try:
        return json.loads(request.body or b"{}")
    except ValueError:
        return {}


def has_order(model):
    return any(f.name == "order" for f in model._meta.get_fields())


def tab_fields(res):
    out = []
    for _, fields in res["tabs"]:
        out += [f for f in fields if not f.startswith("@")]
    return out


def editable_fields(res):
    ro = set(res.get("readonly", []))
    return [f for f in tab_fields(res) if f not in ro]


def fk_to(child_model, parent_model):
    for f in child_model._meta.get_fields():
        if getattr(f, "many_to_one", False) and f.related_model is parent_model:
            return f.name
    raise LookupError


def save_form(model, names, request, instance=None, extra=None):
    """Django ModelForm orqali saqlash: validatsiya, fayllar, M2M — hammasi standart."""
    fields = form_field_names(model, names)
    Form = modelform_factory(model, fields=fields)
    data = request.POST.copy()
    for k, v in (extra or {}).items():
        data[k] = v
    form = Form(data, request.FILES, instance=instance)
    if not form.is_valid():
        return None, form.errors.get_json_data()
    with transaction.atomic():
        obj = form.save()
    return obj, None


def errors_by_base(errors):
    """name_en / name_ru xatolarini frontend uchun soddalashtirish."""
    out = {}
    for k, lst in errors.items():
        out[k] = [e["message"] for e in lst]
    return out


# ---------------------------------------------------------------- auth

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"ok": True})


@require_http_methods(["POST"])
def login_view(request):
    data = body_json(request)
    user = authenticate(request, username=data.get("username", "").strip(), password=data.get("password", ""))
    if not user or not user.is_staff or not user.is_active:
        return err("Неверный логин или пароль", 400)
    login(request, user)
    return JsonResponse({"ok": True})


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({"ok": True})


@staff_required
def me(request):
    u = request.user
    nav = []
    for g in GROUPS:
        items = []
        for key, res in RESOURCES.items():
            if res["group"] != g or not can(u, res["model"], "view"):
                continue
            item = {"key": key, "title": res["title"], "icon": res["icon"], "singleton": res.get("singleton", False)}
            if res.get("badge"):
                item["badge"] = res["model"].objects.filter(status=res["badge"]).count()
            items.append(item)
        if items:
            nav.append({"title": g, "items": items})
    return JsonResponse({
        "user": {"username": u.username, "name": u.get_full_name() or u.username, "superuser": u.is_superuser},
        "nav": nav,
    })


@staff_required
@require_http_methods(["POST"])
def change_password(request):
    data = body_json(request)
    if not request.user.check_password(data.get("old", "")):
        return err("Старый пароль неверный")
    new = data.get("new", "")
    if len(new) < 10:
        return err("Новый пароль — минимум 10 символов")
    request.user.set_password(new)
    request.user.save()
    update_session_auth_hash(request, request.user)
    return JsonResponse({"ok": True})


# ---------------------------------------------------------------- dashboard

@staff_required
def dashboard(request):
    now = timezone.now()
    recent = Inquiry.objects.select_related("event_type")[:8]
    return JsonResponse({
        "kpis": [
            {"label": "Новые заявки", "value": Inquiry.objects.filter(status="new").count(), "link": "inquiries?status=new", "accent": True},
            {"label": "Заявок за 7 дней", "value": Inquiry.objects.filter(created_at__gte=now - timedelta(days=7)).count(), "link": "inquiries"},
            {"label": "Заявок за 30 дней", "value": Inquiry.objects.filter(created_at__gte=now - timedelta(days=30)).count(), "link": "inquiries"},
            {"label": "Новые партнёры", "value": PartnerRequest.objects.filter(status="new").count(), "link": "partner-requests?status=new"},
        ],
        "recent": [
            {"id": i.id, "created_at": timezone.localtime(i.created_at).strftime("%d.%m %H:%M"), "name": i.name,
             "phone": i.phone, "event_type": str(i.event_type or ""), "guests": i.guests,
             "status": i.status, "status_label": i.get_status_display(), "source": i.source_label}
            for i in recent
        ],
        "counts": {
            "packages": CateringPackage.objects.filter(is_published=True).count(),
            "projects": PortfolioProject.objects.filter(is_published=True).count(),
            "offers": SeasonalOffer.objects.active().count(),
        },
    })


# ---------------------------------------------------------------- resources

def schema_payload(res, user):
    model = res["model"]
    ro = set(res.get("readonly", []))
    fields = {}
    tabs = []
    for title, names in res["tabs"]:
        tab = {"title": title, "fields": []}
        for n in names:
            if n.startswith("@"):
                rel = n[1:]
                ch = res["children"][rel]
                cmodel = ch["model"]
                tab["fields"].append({"child": rel, "title": ch["title"], "upload": ch.get("upload"),
                                      "orderable": has_order(cmodel),
                                      "fields": [field_def(cmodel, f) for f in ch["fields"]]})
            else:
                fields[n] = field_def(model, n, readonly=n in ro)
                tab["fields"].append(n)
        tabs.append(tab)
    if ro:
        extra = [n for n in res.get("readonly", []) if n not in fields]
        for n in extra:
            fields[n] = field_def(model, n, readonly=True)
        if extra:
            tabs.insert(0, {"title": "Данные", "fields": extra, "readonly": True})
    return {
        "key": res["key"], "title": res["title"], "one": res.get("one", res["title"]),
        "singleton": res.get("singleton", False), "fields": fields, "tabs": tabs,
        "list": [field_def(model, n) for n in res.get("list", [])],
        "filters": [field_def(model, n) for n in res.get("filters", [])],
        "search": bool(res.get("search")),
        "orderable": has_order(model) and not res.get("singleton"),
        "can_add": res.get("can_add", True) and not res.get("singleton") and can(user, model, "add"),
        "can_delete": res.get("can_delete", True) and not res.get("singleton") and can(user, model, "delete"),
        "can_change": can(user, model, "change"),
        "export": res.get("export", False),
        "slug_from": res.get("slug_from"),
        "view_on_site": bool(getattr(model, "get_absolute_url", None)),
    }


@staff_required
def schema(request, key):
    res = get_resource(key)
    if not res or not can(request.user, res["model"], "view"):
        return err("not_found", 404)
    return JsonResponse(schema_payload(res, request.user))


def filtered_qs(res, request):
    model = res["model"]
    qs = model.objects.all()
    q = request.GET.get("q", "").strip()
    if q and res.get("search"):
        cond = Q()
        for f in res["search"]:
            cond |= Q(**{f"{f}__icontains": q})
        qs = qs.filter(cond)
    for f in res.get("filters", []):
        v = request.GET.get(f)
        if v not in (None, ""):
            qs = qs.filter(**{f: v})
    if has_order(model):
        qs = qs.order_by("order", "id")
    return qs


@staff_required
def collection(request, key):
    res = get_resource(key)
    if not res:
        return err("not_found", 404)
    model = res["model"]

    if request.method == "GET":
        if not can(request.user, model, "view"):
            return err("forbidden", 403)
        if res.get("singleton"):
            return JsonResponse({"singleton": True, "id": model.load().pk})
        qs = filtered_qs(res, request)
        page = Paginator(qs, PAGE_SIZE).get_page(request.GET.get("page") or 1)
        return JsonResponse({
            "total": page.paginator.count, "page": page.number, "pages": page.paginator.num_pages,
            "rows": [{"id": o.pk, "str": str(o), "cells": {n: display_value(o, n) for n in res.get("list", [])}}
                     for o in page.object_list],
        })

    if request.method == "POST":
        if not res.get("can_add", True) or res.get("singleton") or not can(request.user, model, "add"):
            return err("forbidden", 403)
        obj, errors = save_form(model, editable_fields(res), request)
        if obj and has_order(model):  # yangi yozuv ro'yxat oxiriga
            last = model.objects.exclude(pk=obj.pk).order_by("-order").values_list("order", flat=True).first() or 0
            model.objects.filter(pk=obj.pk).update(order=last + 1)
        if errors:
            return err("validation", 400, errors=errors_by_base(errors))
        return JsonResponse({"ok": True, "id": obj.pk}, status=201)

    return err("method", 405)


def item_payload(res, obj):
    names = tab_fields(res) + [n for n in res.get("readonly", []) if n not in tab_fields(res)]
    values = {n: field_value(obj, n) for n in names}
    children = {}
    for rel, ch in res.get("children", {}).items():
        cmodel = ch["model"]
        qs = getattr(obj, rel).all()
        if has_order(cmodel):
            qs = qs.order_by("order", "id")
        children[rel] = [{"id": c.pk, "values": {f: field_value(c, f) for f in ch["fields"]}} for c in qs]
    url = obj.get_absolute_url() if hasattr(obj, "get_absolute_url") else None
    return {"id": obj.pk, "str": str(obj), "values": values, "children": children, "url": url}


@staff_required
def item(request, key, pk):
    res = get_resource(key)
    if not res:
        return err("not_found", 404)
    model = res["model"]
    obj = model.load() if res.get("singleton") else model.objects.filter(pk=pk).first()
    if not obj:
        return err("not_found", 404)

    if request.method == "GET":
        if not can(request.user, model, "view"):
            return err("forbidden", 403)
        return JsonResponse(item_payload(res, obj))

    if request.method == "POST":  # yangilash (multipart)
        if not can(request.user, model, "change"):
            return err("forbidden", 403)
        obj, errors = save_form(model, editable_fields(res), request, instance=obj)
        if errors:
            return err("validation", 400, errors=errors_by_base(errors))
        return JsonResponse({"ok": True, **item_payload(res, obj)})

    if request.method == "DELETE":
        if res.get("singleton") or not res.get("can_delete", True) or not can(request.user, model, "delete"):
            return err("forbidden", 403)
        obj.delete()
        return JsonResponse({"ok": True})

    return err("method", 405)


@staff_required
@require_http_methods(["POST"])
def toggle(request, key, pk):
    """Ro'yxatdan turib "Показывать" kabi galochkani almashtirish."""
    res = get_resource(key)
    field = body_json(request).get("field")
    if not res or field not in res.get("list", []) or not can(request.user, res["model"], "change"):
        return err("forbidden", 403)
    obj = res["model"].objects.filter(pk=pk).first()
    if not obj or not isinstance(getattr(obj, field, None), bool):
        return err("bad_field")
    setattr(obj, field, not getattr(obj, field))
    obj.save(update_fields=[field] + (["updated_at"] if hasattr(obj, "updated_at") else []))
    return JsonResponse({"ok": True, "value": getattr(obj, field)})


@staff_required
@require_http_methods(["POST"])
def reorder(request, key):
    res = get_resource(key)
    if not res or not has_order(res["model"]) or not can(request.user, res["model"], "change"):
        return err("forbidden", 403)
    ids = body_json(request).get("ids", [])
    with transaction.atomic():
        for i, pk in enumerate(ids):
            res["model"].objects.filter(pk=pk).update(order=i)
    # ro'yxat tartibi saytda darhol yangilansin
    from apps.core.signals import trigger_revalidate
    trigger_revalidate()
    return JsonResponse({"ok": True})


@staff_required
def export(request, key):
    res = get_resource(key)
    if not res or not res.get("export") or not can(request.user, res["model"], "view"):
        return err("forbidden", 403)
    model = res["model"]
    names = res.get("readonly", []) + ["status", "manager_note"]
    resp = HttpResponse(content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = f'attachment; filename="rokate-{key}-{timezone.localdate():%Y%m%d}.csv"'
    resp.write("﻿")
    w = csv.writer(resp, delimiter=";")
    w.writerow([str(model._meta.get_field(n).verbose_name) for n in names])
    for o in filtered_qs(res, request):
        row = []
        for n in names:
            disp = getattr(o, f"get_{n}_display", None)
            v = disp() if disp else getattr(o, n)
            row.append("" if v is None else str(plain(v)))
        w.writerow(row)
    return resp


# ---------------------------------------------------------------- children (galereya, qadamlar, menyu pozitsiyalari)

def child_ctx(request, key, pk, rel):
    res = get_resource(key)
    if not res or rel not in res.get("children", {}):
        return None, None, None, err("not_found", 404)
    model = res["model"]
    if not can(request.user, model, "change"):
        return None, None, None, err("forbidden", 403)
    parent = model.load() if res.get("singleton") else model.objects.filter(pk=pk).first()
    if not parent:
        return None, None, None, err("not_found", 404)
    return res, res["children"][rel], parent, None


@staff_required
@require_http_methods(["POST"])
def child_create(request, key, pk, rel):
    res, ch, parent, e = child_ctx(request, key, pk, rel)
    if e:
        return e
    cmodel = ch["model"]
    fk = fk_to(cmodel, type(parent))
    start = getattr(parent, rel).count()
    created = []
    upload = ch.get("upload")
    files = request.FILES.getlist("files") if upload else []
    if upload and files:
        title_en = getattr(parent, "title_en", None) or getattr(parent, "name_en", None) or ""
        title_ru = getattr(parent, "title_ru", None) or getattr(parent, "name_ru", None) or ""
        for i, f in enumerate(files):
            kwargs = {fk: parent, upload: f}
            if has_order(cmodel):
                kwargs["order"] = start + i
            if "alt" in ch["fields"]:
                kwargs.update(alt_en=title_en, alt_ru=title_ru)
            obj = cmodel(**kwargs)
            try:
                obj.full_clean(exclude=[fk])
            except Exception as exc:  # noqa: BLE001
                return err(f"{f.name}: {exc}")
            obj.save()
            created.append(obj.pk)
    else:
        extra = {fk: parent.pk}
        if has_order(cmodel):
            extra["order"] = start
        obj, errors = save_form(cmodel, ch["fields"] + [fk] + (["order"] if has_order(cmodel) else []), request, extra=extra)
        if errors:
            return err("validation", 400, errors=errors_by_base(errors))
        created.append(obj.pk)
    return JsonResponse({"ok": True, "created": created, **item_payload(res, parent)}, status=201)


@staff_required
@require_http_methods(["POST", "DELETE"])
def child_item(request, key, pk, rel, cid):
    res, ch, parent, e = child_ctx(request, key, pk, rel)
    if e:
        return e
    obj = getattr(parent, rel).filter(pk=cid).first()
    if not obj:
        return err("not_found", 404)
    if request.method == "DELETE":
        obj.delete()
    else:
        obj, errors = save_form(ch["model"], ch["fields"], request, instance=obj)
        if errors:
            return err("validation", 400, errors=errors_by_base(errors))
    return JsonResponse({"ok": True, **item_payload(res, parent)})


@staff_required
@require_http_methods(["POST"])
def child_reorder(request, key, pk, rel):
    res, ch, parent, e = child_ctx(request, key, pk, rel)
    if e:
        return e
    ids = body_json(request).get("ids", [])
    with transaction.atomic():
        for i, cid in enumerate(ids):
            getattr(parent, rel).filter(pk=cid).update(order=i)
    from apps.core.signals import trigger_revalidate
    trigger_revalidate()
    return JsonResponse({"ok": True, **item_payload(res, parent)})
