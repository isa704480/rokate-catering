from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.base import Publishable, SEOFields, Singleton, TimeStamped


class CateringPackage(Publishable, SEOFields, TimeStamped):
    BADGES = [("", "—"), ("new", "New"), ("seasonal", "Seasonal"), ("bestseller", "Bestseller"), ("signature", "Signature")]

    name = models.CharField("Название", max_length=120)
    slug = models.SlugField("Код (slug)", unique=True)
    image = models.ImageField("Фото", upload_to="packages/", blank=True)
    guests_min = models.PositiveIntegerField("Гостей от", null=True, blank=True)
    guests_max = models.PositiveIntegerField("Гостей до", null=True, blank=True)
    short_text = models.CharField("Короткое описание", max_length=240, blank=True)
    contents = models.TextField("Состав", blank=True, help_text="Каждая позиция с новой строки.")
    price_from = models.DecimalField(
        "Цена от (AED)", max_digits=10, decimal_places=0, null=True, blank=True,
        help_text="Если пусто — на сайте будет «Цена по запросу».",
    )
    price_note = models.CharField("Пояснение к цене", max_length=60, blank=True, help_text="Например: per person / за сет")
    badge = models.CharField("Метка", max_length=12, choices=BADGES, blank=True)
    is_featured = models.BooleanField("Показывать на главной", default=True)

    class Meta(Publishable.Meta):
        verbose_name = "Готовый пакет"
        verbose_name_plural = "Готовые пакеты"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{settings.SITE_URL}/#packages"


class PackageImage(models.Model):
    package = models.ForeignKey(CateringPackage, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Фото", upload_to="packages/")
    alt = models.CharField("Описание фото (alt)", max_length=160, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Доп. фото"
        verbose_name_plural = "Дополнительные фото"


class SeasonalOfferQuerySet(models.QuerySet):
    def active(self):
        today = timezone.localdate()
        return self.filter(is_published=True).filter(
            models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=today),
            models.Q(ends_at__isnull=True) | models.Q(ends_at__gte=today),
        )


class SeasonalOffer(Publishable, TimeStamped):
    title = models.CharField("Заголовок", max_length=160)
    text = models.TextField("Текст", blank=True)
    image = models.ImageField("Фото", upload_to="offers/", blank=True)
    price = models.DecimalField("Цена (AED)", max_digits=10, decimal_places=0, null=True, blank=True)
    starts_at = models.DateField("Показывать с", null=True, blank=True)
    ends_at = models.DateField("Показывать до", null=True, blank=True, help_text="После этой даты предложение скроется само.")
    cta_text = models.CharField("Текст кнопки", max_length=60, blank=True)
    package = models.ForeignKey(CateringPackage, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Связанный пакет")

    objects = SeasonalOfferQuerySet.as_manager()

    class Meta(Publishable.Meta):
        verbose_name = "Сезонное предложение"
        verbose_name_plural = "Сезонные предложения"

    def __str__(self):
        return self.title


class MenuCategory(Publishable):
    name = models.CharField("Категория", max_length=120)

    class Meta(Publishable.Meta):
        verbose_name = "Категория меню"
        verbose_name_plural = "Меню: категории и позиции"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{settings.SITE_URL}/menu"


class MenuItem(Publishable):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name="items", verbose_name="Категория")
    name = models.CharField("Название", max_length=160)
    description = models.CharField("Описание", max_length=300, blank=True)
    price = models.DecimalField("Цена (AED)", max_digits=10, decimal_places=0, null=True, blank=True)
    is_available = models.BooleanField("В наличии", default=True)

    class Meta(Publishable.Meta):
        verbose_name = "Позиция меню"
        verbose_name_plural = "Позиции меню"

    def __str__(self):
        return self.name


class MenuFile(Singleton, TimeStamped):
    intro = models.TextField("Текст над меню", blank=True)
    pdf_en = models.FileField("PDF меню (EN)", upload_to="menu/", blank=True)
    pdf_ru = models.FileField("PDF меню (RU)", upload_to="menu/", blank=True)

    class Meta:
        verbose_name = "Меню: PDF и текст"
        verbose_name_plural = "Меню: PDF и текст"

    def __str__(self):
        return "Меню: PDF и текст"

    def get_absolute_url(self):
        return f"{settings.SITE_URL}/menu"
