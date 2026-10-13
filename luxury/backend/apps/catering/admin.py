from django.contrib import admin

from apps.core.admin_utils import SingletonAdminMixin, TrAdmin, TrTabularInline, thumb, tr_fieldsets

from .models import CateringPackage, MenuCategory, MenuFile, MenuItem, PackageImage, SeasonalOffer


class PackageImageInline(TrTabularInline):
    model = PackageImage
    fields = ("image", "alt_en", "alt_ru", "order")
    ordering_field = "order"
    hide_ordering_field = True
    tab = True


@admin.register(CateringPackage)
class CateringPackageAdmin(TrAdmin):
    list_display = ("preview", "name", "guests", "price", "badge", "is_featured", "is_published")
    list_display_links = ("preview", "name")
    list_editable = ("is_featured", "is_published")
    list_filter = ("is_published", "is_featured", "badge")
    search_fields = ("name_en", "name_ru")
    ordering_field = "order"
    hide_ordering_field = True
    prepopulated_fields = {"slug": ("name_en",)}
    inlines = [PackageImageInline]
    fieldsets = tr_fieldsets(
        common=("slug", "image", ("guests_min", "guests_max"), "price_from", "badge", "is_featured", "is_published"),
        translated=("name", "short_text", "contents", "price_note"),
        seo=True,
    )

    @admin.display(description="Фото")
    def preview(self, obj):
        return thumb(obj.image)

    @admin.display(description="Гостей")
    def guests(self, obj):
        if obj.guests_min and obj.guests_max:
            return f"{obj.guests_min}–{obj.guests_max}"
        return obj.guests_min or obj.guests_max or "—"

    @admin.display(description="Цена от")
    def price(self, obj):
        return f"{obj.price_from:.0f} AED" if obj.price_from is not None else "по запросу"


@admin.register(SeasonalOffer)
class SeasonalOfferAdmin(TrAdmin):
    list_display = ("preview", "title", "starts_at", "ends_at", "is_published")
    list_display_links = ("preview", "title")
    list_editable = ("is_published",)
    ordering_field = "order"
    hide_ordering_field = True
    fieldsets = tr_fieldsets(
        common=("image", "price", ("starts_at", "ends_at"), "package", "is_published"),
        translated=("title", "text", "cta_text"),
    )

    @admin.display(description="Фото")
    def preview(self, obj):
        return thumb(obj.image)


class MenuItemInline(TrTabularInline):
    model = MenuItem
    fields = ("name_en", "description_en", "name_ru", "description_ru", "price", "is_available", "is_published", "order")
    ordering_field = "order"
    hide_ordering_field = True


@admin.register(MenuCategory)
class MenuCategoryAdmin(TrAdmin):
    list_display = ("name", "items_count", "is_published")
    list_editable = ("is_published",)
    ordering_field = "order"
    hide_ordering_field = True
    inlines = [MenuItemInline]
    fieldsets = tr_fieldsets(common=("is_published",), translated=("name",))

    @admin.display(description="Позиций")
    def items_count(self, obj):
        return obj.items.count()


@admin.register(MenuFile)
class MenuFileAdmin(SingletonAdminMixin, TrAdmin):
    fieldsets = tr_fieldsets(common=("pdf_en", "pdf_ru"), translated=("intro",))
