from modeltranslation.translator import TranslationOptions, register

from .models import (AdditionalService, FAQItem, HomePage, HomeStat, HomeStep, LegalPage,
                     PartnersPage, SiteSettings, WhyUsItem)

SEO = ("seo_title", "seo_description")


@register(SiteSettings)
class SiteSettingsTR(TranslationOptions):
    fields = ("tagline", "whatsapp_text", "service_area", "working_hours", "address",
              "default_seo_title", "default_seo_description")


@register(HomePage)
class HomePageTR(TranslationOptions):
    fields = ("hero_eyebrow", "hero_title", "hero_subtitle", "hero_cta",
              "about_eyebrow", "about_title", "about_text",
              "directions_title", "formats_title", "formats_list",
              "packages_title", "packages_text",
              "relax_eyebrow", "relax_title", "relax_text",
              "services_title", "services_text", "services_note",
              "portfolio_title", "portfolio_text", "why_title", "faq_title",
              "form_title", "form_text") + SEO


@register(HomeStat)
class HomeStatTR(TranslationOptions):
    fields = ("label",)


@register(HomeStep)
class HomeStepTR(TranslationOptions):
    fields = ("title", "text")


@register(WhyUsItem)
class WhyUsItemTR(TranslationOptions):
    fields = ("title", "text")


@register(AdditionalService)
class AdditionalServiceTR(TranslationOptions):
    fields = ("title", "description")


@register(FAQItem)
class FAQItemTR(TranslationOptions):
    fields = ("question", "answer")


@register(PartnersPage)
class PartnersPageTR(TranslationOptions):
    fields = ("title", "intro", "audience_title", "audience", "offer_title", "offer_text", "form_title") + SEO


@register(LegalPage)
class LegalPageTR(TranslationOptions):
    fields = ("title", "body") + SEO
