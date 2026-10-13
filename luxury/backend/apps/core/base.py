"""Umumiy abstrakt modellar va tanlovlar."""
from django.db import models


LOCATION_CHOICES = [
    ("yacht", "Яхта"),
    ("villa", "Вилла"),
    ("office", "Офис"),
    ("home", "Дом"),
    ("desert", "Пустыня / outdoor"),
    ("venue", "Площадка"),
    ("other", "Другое"),
]

# Saytda inline SVG sifatida chiziladigan ikonlar (frontend/components/Icon.tsx)
ICON_CHOICES = [
    ("chef", "Повар"),
    ("yacht", "Яхта"),
    ("villa", "Вилла"),
    ("office", "Офис"),
    ("desert", "Пустыня"),
    ("glass", "Бокал"),
    ("plate", "Посуда / сервировка"),
    ("chair", "Мебель"),
    ("flower", "Цветы"),
    ("balloon", "Шары"),
    ("camera", "Фото / видео"),
    ("music", "DJ / музыка"),
    ("car", "Автомобиль"),
    ("sparkle", "Декор"),
    ("people", "Персонал"),
    ("star", "Звезда"),
    ("clock", "Время"),
    ("shield", "Надёжность"),
    ("leaf", "Свежесть"),
    ("calendar", "Календарь"),
    ("key", "Под ключ"),
    ("frame", "Фотозона"),
]


class TimeStamped(models.Model):
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        abstract = True


class Publishable(models.Model):
    is_published = models.BooleanField("Показывать на сайте", default=True)
    order = models.PositiveIntegerField("Порядок", default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class SEOFields(models.Model):
    seo_title = models.CharField(
        "SEO Title", max_length=70, blank=True,
        help_text="До 60 символов. Если пусто — берётся из названия.",
    )
    seo_description = models.CharField(
        "Meta Description", max_length=170, blank=True,
        help_text="До 160 символов. Если пусто — берётся из краткого описания.",
    )
    og_image = models.ImageField(
        "Картинка для соцсетей (OG)", upload_to="og/", blank=True,
        help_text="Показывается при отправке ссылки в WhatsApp / Instagram. 1200×630.",
    )
    noindex = models.BooleanField("Скрыть от Google (noindex)", default=False)

    class Meta:
        abstract = True


class Singleton(models.Model):
    """Faqat bitta yozuvga ega model (sozlamalar, bosh sahifa)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):  # o'chirib bo'lmaydi
        return None

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


def lines(text):
    """Ko'p qatorli matnni ro'yxatga aylantiradi (bo'sh qatorlarsiz)."""
    return [ln.strip(" •-\t") for ln in (text or "").splitlines() if ln.strip(" •-\t")]
