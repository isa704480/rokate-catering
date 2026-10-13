from django.conf import settings
from django.db import models

from apps.core.base import LOCATION_CHOICES, Publishable, SEOFields, TimeStamped


class EventType(Publishable):
    name = models.CharField("Название", max_length=80)
    slug = models.SlugField("Код", unique=True)

    class Meta(Publishable.Meta):
        verbose_name = "Тип мероприятия"
        verbose_name_plural = "Типы мероприятий"

    def __str__(self):
        return self.name


class ServicePage(Publishable, SEOFields, TimeStamped):
    title = models.CharField("Название", max_length=120, help_text="Например: Yacht Catering")
    slug = models.SlugField("Адрес страницы (slug)", unique=True, help_text="Например: yacht-catering → /catering/yacht-catering")
    card_text = models.CharField("Текст карточки на главной", max_length=220, blank=True)
    location_type = models.CharField("Тип локации", max_length=10, choices=LOCATION_CHOICES, blank=True)
    hero_image = models.ImageField("Фото", upload_to="services/")
    show_on_home = models.BooleanField("Показывать на главной", default=True)
    has_page = models.BooleanField(
        "Отдельная страница", default=True,
        help_text="Выключите, если пока мало контента — карточка на главной будет вести к форме заявки.",
    )
    headline = models.CharField("Заголовок страницы (H1)", max_length=160, blank=True, help_text="Например: Yacht Catering in Dubai")
    intro = models.TextField("Вступление", blank=True)
    body = models.TextField("Основной текст", blank=True, help_text="Абзацы разделяйте пустой строкой.")
    packages = models.ManyToManyField("catering.CateringPackage", blank=True, verbose_name="Подходящие пакеты", related_name="services")
    projects = models.ManyToManyField("portfolio.PortfolioProject", blank=True, verbose_name="Проекты для галереи", related_name="services")

    class Meta(Publishable.Meta):
        verbose_name = "Направление / страница услуги"
        verbose_name_plural = "Направления / страницы услуг"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"{settings.SITE_URL}/catering/{self.slug}"


class ServiceOption(models.Model):
    service = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name="options")
    title = models.CharField("Название", max_length=120)
    text = models.TextField("Описание", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Вариант обслуживания"
        verbose_name_plural = "Варианты обслуживания"

    def __str__(self):
        return self.title
