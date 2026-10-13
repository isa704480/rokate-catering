from modeltranslation.translator import TranslationOptions, register

from .models import EventType, ServiceOption, ServicePage


@register(EventType)
class EventTypeTR(TranslationOptions):
    fields = ("name",)


@register(ServicePage)
class ServicePageTR(TranslationOptions):
    fields = ("title", "card_text", "headline", "intro", "body", "seo_title", "seo_description")


@register(ServiceOption)
class ServiceOptionTR(TranslationOptions):
    fields = ("title", "text")
