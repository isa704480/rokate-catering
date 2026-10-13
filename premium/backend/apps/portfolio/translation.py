from modeltranslation.translator import TranslationOptions, register

from .models import PortfolioImage, PortfolioProject


@register(PortfolioProject)
class PortfolioProjectTR(TranslationOptions):
    fields = ("title", "description", "seo_title", "seo_description")


@register(PortfolioImage)
class PortfolioImageTR(TranslationOptions):
    fields = ("alt",)
