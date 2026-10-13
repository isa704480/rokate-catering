from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .admin_utils import SingletonAdminMixin, TrAdmin, TrTabularInline, thumb, tr_fieldsets
from .models import (AdditionalService, FAQItem, HomePage, HomeStat, HomeStep, LegalPage, PartnersPage,
                     SiteSettings, WhyUsItem)

# --- Foydalanuvchilar (Unfold uslubida) ------------------------------------
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


# --- Sozlamalar --------------------------------------------------------------
@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdminMixin, TrAdmin):
    fieldsets = tr_fieldsets(
        common=("company_name", "phone", "whatsapp_number", "email", "instagram_url", "logo"),
        translated=("tagline", "whatsapp_text", "service_area", "working_hours", "address"),
        extra=(
            ("Уведомления о заявках", ("notify_emails", "telegram_chat_id")),
            ("SEO по умолчанию", ("default_seo_title_en", "default_seo_description_en",
                                  "default_seo_title_ru", "default_seo_description_ru", "default_og_image")),
        ),
    )


# --- Bosh sahifa -----------------------------------------------------------
class HomeStatInline(TrTabularInline):
    model = HomeStat
    fields = ("value", "label_en", "label_ru", "order")
    ordering_field = "order"
    hide_ordering_field = True
    tab = True


class HomeStepInline(TrTabularInline):
    model = HomeStep
    fields = ("title_en", "text_en", "title_ru", "text_ru", "order")
    ordering_field = "order"
    hide_ordering_field = True
    tab = True


class WhyUsInline(TrTabularInline):
    model = WhyUsItem
    fields = ("icon", "title_en", "text_en", "title_ru", "text_ru", "order")
    ordering_field = "order"
    hide_ordering_field = True
    tab = True


HOME_TEXT = (
    "hero_eyebrow", "hero_title", "hero_subtitle", "hero_cta",
    "about_eyebrow", "about_title", "about_text",
    "directions_title", "formats_title", "formats_list",
    "packages_title", "packages_text",
    "relax_eyebrow", "relax_title", "relax_text",
    "services_title", "services_text", "services_note",
    "portfolio_title", "portfolio_text", "why_title", "faq_title",
    "form_title", "form_text",
)


@admin.register(HomePage)
class HomePageAdmin(SingletonAdminMixin, TrAdmin):
    inlines = [HomeStatInline, HomeStepInline, WhyUsInline]
    fieldsets = tr_fieldsets(
        common=("hero_image", "hero_video", "about_image", "relax_image"),
        translated=HOME_TEXT,
        seo=True,
    )


# --- Qo'shimcha xizmatlar, FAQ ------------------------------------------------
@admin.register(AdditionalService)
class AdditionalServiceAdmin(TrAdmin):
    list_display = ("title", "icon", "provider", "is_published")
    list_filter = ("provider", "is_published")
    list_editable = ("is_published",)
    ordering_field = "order"
    hide_ordering_field = True
    fieldsets = tr_fieldsets(common=("icon", "provider", "is_published"), translated=("title", "description"))


@admin.register(FAQItem)
class FAQItemAdmin(TrAdmin):
    list_display = ("question", "placement", "service", "is_published")
    list_filter = ("placement", "is_published")
    list_editable = ("is_published",)
    ordering_field = "order"
    hide_ordering_field = True
    fieldsets = tr_fieldsets(common=("placement", "service", "is_published"), translated=("question", "answer"))


@admin.register(PartnersPage)
class PartnersPageAdmin(SingletonAdminMixin, TrAdmin):
    fieldsets = tr_fieldsets(
        common=("image",),
        translated=("title", "intro", "audience_title", "audience", "offer_title", "offer_text", "form_title"),
        seo=True,
    )


@admin.register(LegalPage)
class LegalPageAdmin(TrAdmin):
    list_display = ("title", "slug", "updated_at")
    fieldsets = tr_fieldsets(common=("slug",), translated=("title", "body"), seo=True)


__all__ = ["thumb"]
