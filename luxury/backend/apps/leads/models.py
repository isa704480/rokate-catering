from django.db import models

from apps.core.base import LOCATION_CHOICES

STATUS_CHOICES = [
    ("new", "🆕 Новая"),
    ("contacted", "💬 На связи"),
    ("won", "✅ Договорились"),
    ("lost", "❌ Отказ"),
    ("spam", "🗑 Спам"),
]


class Inquiry(models.Model):
    name = models.CharField("Имя", max_length=120)
    phone = models.CharField("Телефон / WhatsApp", max_length=40)
    event_date = models.DateField("Дата мероприятия", null=True, blank=True)
    event_type = models.ForeignKey(
        "services.EventType", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тип мероприятия"
    )
    guests = models.PositiveIntegerField("Гостей", null=True, blank=True)
    location_type = models.CharField("Локация", max_length=10, choices=LOCATION_CHOICES, blank=True)
    comment = models.TextField("Комментарий", blank=True)
    package = models.ForeignKey(
        "catering.CateringPackage", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пакет"
    )

    # Откуда пришёл клиент (аналитика)
    language = models.CharField("Язык", max_length=5, blank=True)
    source_page = models.CharField("Страница", max_length=300, blank=True)
    utm_source = models.CharField("utm_source", max_length=120, blank=True)
    utm_medium = models.CharField("utm_medium", max_length=120, blank=True)
    utm_campaign = models.CharField("utm_campaign", max_length=120, blank=True)
    referrer = models.CharField("Referrer", max_length=300, blank=True)

    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default="new", db_index=True)
    manager_note = models.TextField("Заметка менеджера", blank=True)
    created_at = models.DateTimeField("Получена", auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка клиента"
        verbose_name_plural = "Заявки клиентов"

    def __str__(self):
        return f"{self.name} · {self.phone}"

    @property
    def source_label(self):
        if self.utm_source:
            return f"{self.utm_source}/{self.utm_medium}" if self.utm_medium else self.utm_source
        if self.referrer:
            return self.referrer.split("/")[2] if "://" in self.referrer else self.referrer
        return "direct"


class PartnerRequest(models.Model):
    name = models.CharField("Имя", max_length=120)
    company = models.CharField("Компания", max_length=160, blank=True)
    field = models.CharField("Сфера деятельности", max_length=160, blank=True)
    phone = models.CharField("Телефон", max_length=40, blank=True)
    email = models.EmailField("Email", blank=True)
    message = models.TextField("Сообщение", blank=True)
    language = models.CharField("Язык", max_length=5, blank=True)
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default="new", db_index=True)
    manager_note = models.TextField("Заметка менеджера", blank=True)
    created_at = models.DateTimeField("Получена", auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка партнёра"
        verbose_name_plural = "Заявки партнёров"

    def __str__(self):
        return f"{self.name} · {self.company}"
