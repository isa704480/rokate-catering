"""Admin uchun umumiy yordamchilar: tarjima tablari, singleton, rasm preview."""
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline, TranslationTabularInline
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from .images import image_data

EN, RU = "🇬🇧 English", "🇷🇺 Русский"


def tr_fieldsets(common=(), translated=(), seo=False, extra=()):
    """Unfold tablari: Asosiy | English | Русский | (qo'shimcha) | SEO."""
    sets = []
    if common:
        sets.append(("Основное", {"classes": ["tab"], "fields": list(common)}))
    if translated:
        sets.append((EN, {"classes": ["tab"], "fields": [f"{f}_en" for f in translated]}))
        sets.append((RU, {"classes": ["tab"], "fields": [f"{f}_ru" for f in translated]}))
    for title, fields in extra:
        sets.append((title, {"classes": ["tab"], "fields": list(fields)}))
    if seo:
        sets.append(("SEO", {"classes": ["tab"], "fields": [
            "seo_title_en", "seo_description_en", "seo_title_ru", "seo_description_ru", "og_image", "noindex",
        ]}))
    return sets


class TrAdmin(ModelAdmin, TranslationAdmin):
    """Unfold + modeltranslation."""

    warn_unsaved_form = True
    compressed_fields = True


class TrTabularInline(TabularInline, TranslationTabularInline):
    extra = 0


class TrStackedInline(StackedInline, TranslationStackedInline):
    extra = 0


class SingletonAdminMixin:
    """Bitta yozuvli modellar: ro'yxat o'rniga to'g'ridan-to'g'ri tahrirlash sahifasi."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.load()
        opts = self.model._meta
        return HttpResponseRedirect(reverse(f"admin:{opts.app_label}_{opts.model_name}_change", args=[obj.pk]))


def thumb(field, size=64):
    data = image_data(field)
    if not data:
        return "—"
    return format_html(
        '<img src="{}" style="width:{}px;height:{}px;object-fit:cover;border-radius:8px" alt="">',
        data["src"], size, size,
    )
