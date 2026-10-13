"""Admin bosh sahifasi (dashboard) uchun ma'lumotlar."""
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from apps.catering.models import CateringPackage, SeasonalOffer
from apps.leads.models import Inquiry, PartnerRequest
from apps.portfolio.models import PortfolioProject


def dashboard_callback(request, context):
    now = timezone.now()
    week = now - timedelta(days=7)
    month = now - timedelta(days=30)
    context.update({
        "rk_kpis": [
            {"label": "Новые заявки", "value": Inquiry.objects.filter(status="new").count(),
             "url": reverse("admin:leads_inquiry_changelist") + "?status__exact=new"},
            {"label": "Заявок за 7 дней", "value": Inquiry.objects.filter(created_at__gte=week).count(),
             "url": reverse("admin:leads_inquiry_changelist")},
            {"label": "Заявок за 30 дней", "value": Inquiry.objects.filter(created_at__gte=month).count(),
             "url": reverse("admin:leads_inquiry_changelist")},
            {"label": "Новые партнёры", "value": PartnerRequest.objects.filter(status="new").count(),
             "url": reverse("admin:leads_partnerrequest_changelist")},
        ],
        "rk_recent": Inquiry.objects.select_related("event_type")[:8],
        "rk_quick": [
            {"label": "+ Пакет", "url": reverse("admin:catering_cateringpackage_add")},
            {"label": "+ Проект в портфолио", "url": reverse("admin:portfolio_portfolioproject_add")},
            {"label": "+ Сезонное предложение", "url": reverse("admin:catering_seasonaloffer_add")},
            {"label": "Главная страница", "url": reverse("admin:core_homepage_changelist")},
            {"label": "Контакты и настройки", "url": reverse("admin:core_sitesettings_changelist")},
        ],
        "rk_counts": {
            "packages": CateringPackage.objects.filter(is_published=True).count(),
            "projects": PortfolioProject.objects.filter(is_published=True).count(),
            "offers": SeasonalOffer.objects.active().count(),
        },
    })
    return context
