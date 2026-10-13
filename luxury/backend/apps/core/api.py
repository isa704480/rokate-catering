"""Sayt (Next.js) uchun JSON API.

Til: ?lang=en|ru. Tarjima bo'sh bo'lsa EN qaytariladi (modeltranslation fallback).
Faqat is_published=True yozuvlar qaytariladi.
"""
import json
import logging
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import translation
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.catering.models import CateringPackage, MenuCategory, MenuFile, SeasonalOffer
from apps.leads.models import Inquiry, PartnerRequest
from apps.leads.notify import inquiry_text, notify, partner_text
from apps.portfolio.models import PortfolioProject
from apps.services.models import EventType, ServicePage

from .base import LOCATION_CHOICES, lines
from .images import file_url, image_data
from .models import AdditionalService, FAQItem, HomePage, LegalPage, PartnersPage, SiteSettings

log = logging.getLogger(__name__)
LANGS = {"en", "ru"}


def _lang(request):
    lang = request.query_params.get("lang", "en")
    return lang if lang in LANGS else "en"


def with_lang(view):
    def wrapped(request, *args, **kwargs):
        with translation.override(_lang(request)):
            return view(request, *args, **kwargs)

    wrapped.__name__ = view.__name__
    wrapped.__doc__ = view.__doc__
    return wrapped


# --- payload builders --------------------------------------------------------

def seo(obj, title_fallback="", desc_fallback=""):
    return {
        "title": getattr(obj, "seo_title", "") or title_fallback,
        "description": getattr(obj, "seo_description", "") or desc_fallback,
        "image": image_data(getattr(obj, "og_image", None)),
        "noindex": getattr(obj, "noindex", False),
    }


def settings_payload():
    s = SiteSettings.load()
    return {
        "company_name": s.company_name,
        "tagline": s.tagline,
        "phone": s.phone,
        "whatsapp_number": "".join(ch for ch in s.whatsapp_number if ch.isdigit()),
        "whatsapp_text": s.whatsapp_text,
        "email": s.email,
        "instagram_url": s.instagram_url,
        "service_area": s.service_area,
        "working_hours": s.working_hours,
        "address": s.address,
        "logo": file_url(s.logo),
        "seo": {
            "title": s.default_seo_title,
            "description": s.default_seo_description,
            "image": image_data(s.default_og_image),
        },
        "event_types": [{"id": e.id, "slug": e.slug, "name": e.name} for e in EventType.objects.filter(is_published=True)],
        "locations": [{"value": v, "label": label} for v, label in LOCATION_CHOICES],
        "nav_services": [
            {"slug": sp.slug, "title": sp.title}
            for sp in ServicePage.objects.filter(is_published=True, has_page=True)
        ],
    }


def package_payload(p):
    return {
        "id": p.id,
        "slug": p.slug,
        "name": p.name,
        "image": image_data(p.image, p.name),
        "images": [image_data(i.image, i.alt or p.name) for i in p.images.all()],
        "guests_min": p.guests_min,
        "guests_max": p.guests_max,
        "short_text": p.short_text,
        "contents": lines(p.contents),
        "price_from": int(p.price_from) if p.price_from is not None else None,
        "price_note": p.price_note,
        "badge": p.badge,
    }


def project_payload(p, full=False):
    data = {
        "slug": p.slug,
        "title": p.title,
        "location_type": p.location_type,
        "location_label": p.get_location_type_display() if p.location_type else "",
        "event_type": p.event_type.name if p.event_type else "",
        "guests": p.guests,
        "year": p.event_date.year if p.event_date else None,
        "cover": image_data(p.cover, p.title),
        "description": p.description,
        "images": [image_data(i.image, i.alt or p.title) for i in p.images.all()],
        "video_url": p.video_url,
    }
    if full:
        data["seo"] = seo(p, p.title, p.description[:160])
    return data


def service_card(sp):
    return {
        "slug": sp.slug,
        "title": sp.title,
        "card_text": sp.card_text,
        "location_type": sp.location_type,
        "has_page": sp.has_page,
        "image": image_data(sp.hero_image, sp.title),
    }


def offer_payload(o):
    return {
        "id": o.id,
        "title": o.title,
        "text": o.text,
        "image": image_data(o.image, o.title),
        "price": int(o.price) if o.price is not None else None,
        "ends_at": o.ends_at.isoformat() if o.ends_at else None,
        "cta_text": o.cta_text,
        "package": o.package.slug if o.package else None,
    }


def faq_payload(qs):
    return [{"q": f.question, "a": f.answer} for f in qs]


# --- GET endpoints -----------------------------------------------------------

@api_view(["GET"])
@with_lang
def site(request):
    return Response(settings_payload())


@api_view(["GET"])
@with_lang
def home(request):
    h = HomePage.load()
    packages = CateringPackage.objects.filter(is_published=True, is_featured=True).prefetch_related("images")
    projects = (PortfolioProject.objects.filter(is_published=True, is_featured=True)
                .select_related("event_type").prefetch_related("images"))
    return Response({
        "hero": {
            "eyebrow": h.hero_eyebrow,
            "title": h.hero_title,
            "subtitle": h.hero_subtitle,
            "image": image_data(h.hero_image, h.hero_title),
            "video": file_url(h.hero_video),
            "cta": h.hero_cta,
        },
        "about": {
            "eyebrow": h.about_eyebrow,
            "title": h.about_title,
            "text": h.about_text,
            "image": image_data(h.about_image, h.about_title),
            "stats": [{"value": s.value, "label": s.label} for s in h.stats.all()],
        },
        "directions": {
            "title": h.directions_title,
            "items": [service_card(sp) for sp in ServicePage.objects.filter(is_published=True, show_on_home=True)],
        },
        "formats": {"title": h.formats_title, "items": lines(h.formats_list)},
        "packages": {
            "title": h.packages_title,
            "text": h.packages_text,
            "items": [package_payload(p) for p in packages],
        },
        "offers": [offer_payload(o) for o in SeasonalOffer.objects.active().select_related("package")],
        "relax": {
            "eyebrow": h.relax_eyebrow,
            "title": h.relax_title,
            "text": h.relax_text,
            "image": image_data(h.relax_image, h.relax_title),
            "steps": [{"title": s.title, "text": s.text} for s in h.steps.all()],
        },
        "services": {
            "title": h.services_title,
            "text": h.services_text,
            "note": h.services_note,
            "items": [
                {"title": a.title, "description": a.description, "icon": a.icon}
                for a in AdditionalService.objects.filter(is_published=True)
            ],
        },
        "portfolio": {
            "title": h.portfolio_title,
            "text": h.portfolio_text,
            "items": [project_payload(p) for p in projects],
        },
        "why": {
            "title": h.why_title,
            "items": [{"icon": w.icon, "title": w.title, "text": w.text} for w in h.why_items.all()],
        },
        "faq": {
            "title": h.faq_title,
            "items": faq_payload(FAQItem.objects.filter(is_published=True, placement="home")),
        },
        "form": {"title": h.form_title, "text": h.form_text},
        "seo": seo(h, h.hero_title, h.hero_subtitle[:160]),
    })


@api_view(["GET"])
@with_lang
def service_detail(request, slug):
    sp = get_object_or_404(ServicePage, slug=slug, is_published=True, has_page=True)
    projects = sp.projects.filter(is_published=True).prefetch_related("images")
    if not projects and sp.location_type:
        projects = PortfolioProject.objects.filter(is_published=True, location_type=sp.location_type).prefetch_related("images")
    gallery = []
    for p in projects:
        gallery.append(image_data(p.cover, p.title))
        gallery.extend(image_data(i.image, i.alt or p.title) for i in p.images.all())
    return Response({
        "slug": sp.slug,
        "title": sp.title,
        "headline": sp.headline or sp.title,
        "intro": sp.intro,
        "body": sp.body,
        "image": image_data(sp.hero_image, sp.title),
        "location_type": sp.location_type,
        "options": [{"title": o.title, "text": o.text} for o in sp.options.all()],
        "packages": [package_payload(p) for p in sp.packages.filter(is_published=True)],
        "gallery": gallery[:12],
        "faq": faq_payload(sp.faq.filter(is_published=True)),
        "seo": seo(sp, sp.headline or sp.title, (sp.intro or sp.card_text)[:160]),
    })


@api_view(["GET"])
@with_lang
def packages(request):
    qs = CateringPackage.objects.filter(is_published=True).prefetch_related("images")
    return Response([package_payload(p) for p in qs])


@api_view(["GET"])
@with_lang
def menu(request):
    mf = MenuFile.load()
    lang = _lang(request)
    pdf = (mf.pdf_ru if lang == "ru" else None) or mf.pdf_en or mf.pdf_ru
    cats = MenuCategory.objects.filter(is_published=True).prefetch_related("items")
    return Response({
        "intro": mf.intro,
        "pdf": file_url(pdf) if pdf else None,
        "categories": [
            {
                "name": c.name,
                "items": [
                    {"name": i.name, "description": i.description,
                     "price": int(i.price) if i.price is not None else None}
                    for i in c.items.all() if i.is_published and i.is_available
                ],
            }
            for c in cats
        ],
    })


@api_view(["GET"])
@with_lang
def portfolio_detail(request, slug):
    p = get_object_or_404(PortfolioProject, slug=slug, is_published=True)
    return Response(project_payload(p, full=True))


@api_view(["GET"])
@with_lang
def partners(request):
    pp = PartnersPage.load()
    return Response({
        "title": pp.title,
        "intro": pp.intro,
        "audience_title": pp.audience_title,
        "audience": lines(pp.audience),
        "offer_title": pp.offer_title,
        "offer_text": pp.offer_text,
        "image": image_data(pp.image, pp.title),
        "form_title": pp.form_title,
        "faq": faq_payload(FAQItem.objects.filter(is_published=True, placement="partners")),
        "seo": seo(pp, pp.title, pp.intro[:160]),
    })


@api_view(["GET"])
@with_lang
def legal(request, slug):
    lp = LegalPage.objects.filter(slug=slug).first()
    if not lp:
        raise Http404
    return Response({"title": lp.title, "body": lp.body, "seo": seo(lp, lp.title)})


@api_view(["GET"])
def sitemap(request):
    def ts(o):
        return o.updated_at.isoformat()

    home_obj = HomePage.load()
    items = [{"path": "/", "updated": ts(home_obj)}, {"path": "/menu", "updated": ts(MenuFile.load())},
             {"path": "/partners", "updated": ts(PartnersPage.load())}]
    items += [{"path": f"/catering/{s.slug}", "updated": ts(s)}
              for s in ServicePage.objects.filter(is_published=True, has_page=True, noindex=False)]
    items += [{"path": f"/{lp.slug}", "updated": ts(lp)} for lp in LegalPage.objects.filter(noindex=False)]
    return Response(items)


# --- POST endpoints (formalar) ----------------------------------------------

def _client_ip(request):
    return (request.META.get("HTTP_CF_CONNECTING_IP")
            or (request.META.get("HTTP_X_FORWARDED_FOR") or "").split(",")[0].strip()
            or request.META.get("REMOTE_ADDR", ""))


def _rate_limited(request, scope, limit=5, window=3600):
    key = f"rl:{scope}:{_client_ip(request)}"
    count = cache.get(key, 0)
    if count >= limit:
        return True
    cache.set(key, count + 1, window)
    return False


def _turnstile_ok(token, ip):
    secret = settings.TURNSTILE_SECRET_KEY
    if not secret:
        return True
    if not token:
        return False
    try:
        data = urllib.parse.urlencode({"secret": secret, "response": token, "remoteip": ip}).encode()
        with urllib.request.urlopen("https://challenges.cloudflare.com/turnstile/v0/siteverify", data=data, timeout=8) as r:
            return bool(json.loads(r.read()).get("success"))
    except Exception as exc:  # noqa: BLE001
        log.warning("Turnstile verify failed: %s", exc)
        return True  # Cloudflare ishlamay qolsa, arizani yo'qotmaymiz


class InquirySerializer(serializers.ModelSerializer):
    event_type = serializers.SlugRelatedField(slug_field="slug", queryset=EventType.objects.all(), required=False, allow_null=True)
    package = serializers.SlugRelatedField(slug_field="slug", queryset=CateringPackage.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Inquiry
        fields = ["name", "phone", "event_date", "event_type", "guests", "location_type", "comment", "package",
                  "language", "source_page", "utm_source", "utm_medium", "utm_campaign", "referrer"]

    def validate_phone(self, value):
        if sum(ch.isdigit() for ch in value) < 7:
            raise serializers.ValidationError("Invalid phone number")
        return value


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerRequest
        fields = ["name", "company", "field", "phone", "email", "message", "language"]

    def validate(self, attrs):
        if not attrs.get("phone") and not attrs.get("email"):
            raise serializers.ValidationError({"phone": "Phone or email is required"})
        return attrs


def _create(request, serializer_cls, scope, text_fn, subject):
    if request.data.get("website"):  # honeypot — botlar to'ldiradi
        return Response({"ok": True}, status=201)
    if _rate_limited(request, scope):
        return Response({"ok": False, "error": "rate_limited"}, status=429)
    if not _turnstile_ok(request.data.get("turnstile_token"), _client_ip(request)):
        return Response({"ok": False, "error": "captcha"}, status=400)
    ser = serializer_cls(data=request.data)
    if not ser.is_valid():
        return Response({"ok": False, "errors": ser.errors}, status=400)
    obj = ser.save()
    notify(subject, text_fn(obj))
    return Response({"ok": True}, status=201)


@api_view(["POST"])
def create_inquiry(request):
    return _create(request, InquirySerializer, "inq", inquiry_text, "Rokate: новая заявка с сайта")


@api_view(["POST"])
def create_partner_request(request):
    return _create(request, PartnerSerializer, "prt", partner_text, "Rokate: заявка партнёра")
