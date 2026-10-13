from django.contrib import admin

from apps.core.admin_utils import TrAdmin, TrStackedInline, thumb, tr_fieldsets

from .models import EventType, ServiceOption, ServicePage


@admin.register(EventType)
class EventTypeAdmin(TrAdmin):
    list_display = ("name", "slug", "is_published")
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("name_en",)}
    ordering_field = "order"
    hide_ordering_field = True
    fieldsets = tr_fieldsets(common=("slug", "is_published"), translated=("name",))


class ServiceOptionInline(TrStackedInline):
    model = ServiceOption
    fields = ("title_en", "text_en", "title_ru", "text_ru", "order")
    ordering_field = "order"
    hide_ordering_field = True
    tab = True


@admin.register(ServicePage)
class ServicePageAdmin(TrAdmin):
    list_display = ("preview", "title", "slug", "show_on_home", "has_page", "is_published")
    list_display_links = ("preview", "title")
    list_editable = ("show_on_home", "has_page", "is_published")
    ordering_field = "order"
    hide_ordering_field = True
    prepopulated_fields = {"slug": ("title_en",)}
    filter_horizontal = ("packages", "projects")
    inlines = [ServiceOptionInline]
    fieldsets = tr_fieldsets(
        common=("slug", "hero_image", "location_type", "show_on_home", "has_page", "is_published"),
        translated=("title", "card_text", "headline", "intro", "body"),
        extra=(("Пакеты и галерея", ("packages", "projects")),),
        seo=True,
    )

    @admin.display(description="Фото")
    def preview(self, obj):
        return thumb(obj.hero_image)
