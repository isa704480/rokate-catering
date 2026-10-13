from django.conf import settings
from django.db import models

from apps.core.base import LOCATION_CHOICES, Publishable, SEOFields, TimeStamped


class PortfolioProject(Publishable, SEOFields, TimeStamped):
    title = models.CharField("Название", max_length=160)
    slug = models.SlugField("Код (slug)", unique=True)
    event_type = models.ForeignKey(
        "services.EventType", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тип мероприятия"
    )
    location_type = models.CharField("Локация", max_length=10, choices=LOCATION_CHOICES, blank=True)
    event_date = models.DateField("Дата", null=True, blank=True)
    guests = models.PositiveIntegerField("Гостей", null=True, blank=True)
    description = models.TextField("Описание", blank=True)
    cover = models.ImageField("Обложка", upload_to="portfolio/")
    video_url = models.URLField("Ссылка на видео (необязательно)", blank=True)
    is_featured = models.BooleanField("Показывать на главной", default=True)

    class Meta(Publishable.Meta):
        verbose_name = "Проект портфолио"
        verbose_name_plural = "Портфолио"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"{settings.SITE_URL}/#portfolio"


class PortfolioImage(models.Model):
    project = models.ForeignKey(PortfolioProject, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Фото", upload_to="portfolio/")
    alt = models.CharField("Описание фото (alt)", max_length=160, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Фото"
        verbose_name_plural = "Галерея"

    def __str__(self):
        return self.alt or self.image.name
