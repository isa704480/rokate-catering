from django import forms
from django.contrib import admin

from apps.core.admin_utils import TrAdmin, TrTabularInline, thumb, tr_fieldsets

from .models import PortfolioImage, PortfolioProject


class PortfolioImageInline(TrTabularInline):
    model = PortfolioImage
    fields = ("image", "alt_en", "alt_ru", "order")
    ordering_field = "order"
    hide_ordering_field = True
    tab = True


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single = super().clean
        if isinstance(data, (list, tuple)):
            return [single(d, initial) for d in data if d]
        return [single(data, initial)] if data else []


class PortfolioProjectForm(forms.ModelForm):
    bulk_images = MultipleImageField(
        label="Добавить фото пачкой", required=False,
        help_text="Можно выбрать сразу много фото (в т.ч. HEIC с iPhone). Они добавятся в галерею.",
    )

    class Meta:
        model = PortfolioProject
        fields = "__all__"


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(TrAdmin):
    form = PortfolioProjectForm
    list_display = ("preview", "title", "location_type", "event_type", "photos", "is_featured", "is_published")
    list_display_links = ("preview", "title")
    list_editable = ("is_featured", "is_published")
    list_filter = ("location_type", "event_type", "is_published")
    search_fields = ("title_en", "title_ru")
    ordering_field = "order"
    hide_ordering_field = True
    prepopulated_fields = {"slug": ("title_en",)}
    inlines = [PortfolioImageInline]
    fieldsets = tr_fieldsets(
        common=("slug", "cover", "bulk_images", "location_type", "event_type", ("event_date", "guests"), "video_url",
                "is_featured", "is_published"),
        translated=("title", "description"),
        seo=True,
    )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        files = form.cleaned_data.get("bulk_images") or []
        start = form.instance.images.count()
        for i, f in enumerate(files):
            PortfolioImage.objects.create(project=form.instance, image=f, order=start + i,
                                          alt_en=form.instance.title_en or "", alt_ru=form.instance.title_ru or "")
        if files:
            self.message_user(request, f"Добавлено фото: {len(files)}")

    @admin.display(description="Фото")
    def preview(self, obj):
        return thumb(obj.cover)

    @admin.display(description="Фото в галерее")
    def photos(self, obj):
        return obj.images.count()
