import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import action, display

from .models import Inquiry, PartnerRequest

STATUS_COLORS = {"new": "info", "contacted": "warning", "won": "success", "lost": "danger", "spam": "danger"}


def new_inquiries_badge(request):
    n = Inquiry.objects.filter(status="new").count()
    return str(n) if n else None


def new_partner_badge(request):
    n = PartnerRequest.objects.filter(status="new").count()
    return str(n) if n else None


def _wa_link(phone):
    digits = "".join(ch for ch in phone or "" if ch.isdigit())
    if not digits:
        return phone or "—"
    return format_html('<a href="https://wa.me/{}" target="_blank" rel="noopener" '
                       'style="color:#1F8A4C;font-weight:600">{}</a>', digits, phone)


def _export_csv(modeladmin, queryset, fields, filename):
    resp = HttpResponse(content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = f'attachment; filename="{filename}-{timezone.localdate():%Y%m%d}.csv"'
    resp.write("﻿")  # Excel uchun BOM
    writer = csv.writer(resp, delimiter=";")
    writer.writerow([modeladmin.model._meta.get_field(f).verbose_name for f in fields])
    for obj in queryset:
        row = []
        for f in fields:
            val = getattr(obj, f)
            disp = getattr(obj, f"get_{f}_display", None)
            row.append(disp() if disp else ("" if val is None else str(val)))
        writer.writerow(row)
    return resp


class BaseLeadAdmin(ModelAdmin):
    list_filter = ("status", "created_at")
    list_per_page = 50
    date_hierarchy = "created_at"
    actions = ["mark_contacted", "mark_won", "mark_spam", "export_csv"]

    @display(description="Статус", label={k[0]: STATUS_COLORS[k[0]] for k in Inquiry._meta.get_field("status").choices})
    def status_badge(self, obj):
        return obj.status, obj.get_status_display()

    @display(description="Телефон / WhatsApp")
    def phone_link(self, obj):
        return _wa_link(obj.phone)

    @action(description="Отметить: на связи")
    def mark_contacted(self, request, queryset):
        queryset.update(status="contacted")

    @action(description="Отметить: договорились")
    def mark_won(self, request, queryset):
        queryset.update(status="won")

    @action(description="Отметить: спам")
    def mark_spam(self, request, queryset):
        queryset.update(status="spam")


@admin.register(Inquiry)
class InquiryAdmin(BaseLeadAdmin):
    list_display = ("created_at", "name", "phone_link", "event_type", "guests", "event_date", "source", "status_badge")
    list_display_links = ("created_at", "name")
    list_filter = ("status", "event_type", "location_type", "language", "utm_source", "created_at")
    search_fields = ("name", "phone", "comment")
    readonly_fields = ("created_at", "phone_link", "language", "source_page", "utm_source", "utm_medium",
                       "utm_campaign", "referrer")
    fieldsets = (
        ("Заявка", {"fields": ("status", "manager_note", "created_at", "name", "phone_link", "phone",
                               ("event_date", "guests"), ("event_type", "location_type"), "package", "comment")}),
        ("Откуда пришёл клиент", {"classes": ["collapse"], "fields": (
            "language", "source_page", ("utm_source", "utm_medium", "utm_campaign"), "referrer")}),
    )

    @display(description="Источник")
    def source(self, obj):
        return obj.source_label

    @action(description="Экспорт в CSV (Excel)")
    def export_csv(self, request, queryset):
        fields = ["created_at", "status", "name", "phone", "event_date", "event_type", "guests", "location_type",
                  "package", "comment", "language", "source_page", "utm_source", "utm_medium", "utm_campaign",
                  "referrer", "manager_note"]
        return _export_csv(self, queryset, fields, "rokate-inquiries")


@admin.register(PartnerRequest)
class PartnerRequestAdmin(BaseLeadAdmin):
    list_display = ("created_at", "name", "company", "field", "phone_link", "email", "status_badge")
    list_display_links = ("created_at", "name")
    search_fields = ("name", "company", "email", "phone")
    readonly_fields = ("created_at", "phone_link", "language")
    fields = ("status", "manager_note", "created_at", "name", "company", "field", "phone_link", "phone",
              "email", "message", "language")

    @action(description="Экспорт в CSV (Excel)")
    def export_csv(self, request, queryset):
        fields = ["created_at", "status", "name", "company", "field", "phone", "email", "message", "manager_note"]
        return _export_csv(self, queryset, fields, "rokate-partners")
