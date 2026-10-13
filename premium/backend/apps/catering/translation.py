from modeltranslation.translator import TranslationOptions, register

from .models import CateringPackage, MenuCategory, MenuFile, MenuItem, PackageImage, SeasonalOffer


@register(CateringPackage)
class CateringPackageTR(TranslationOptions):
    fields = ("name", "short_text", "contents", "price_note", "seo_title", "seo_description")


@register(PackageImage)
class PackageImageTR(TranslationOptions):
    fields = ("alt",)


@register(SeasonalOffer)
class SeasonalOfferTR(TranslationOptions):
    fields = ("title", "text", "cta_text")


@register(MenuCategory)
class MenuCategoryTR(TranslationOptions):
    fields = ("name",)


@register(MenuItem)
class MenuItemTR(TranslationOptions):
    fields = ("name", "description")


@register(MenuFile)
class MenuFileTR(TranslationOptions):
    fields = ("intro",)
