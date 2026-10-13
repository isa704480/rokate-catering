from django.conf import settings
from django.db import models

from .base import ICON_CHOICES, Publishable, SEOFields, Singleton, TimeStamped


class SiteSettings(Singleton, TimeStamped):
    company_name = models.CharField("Название компании", max_length=120, default="Rokate Catering")
    tagline = models.CharField("Слоган (для футера)", max_length=200, blank=True)
    phone = models.CharField("Телефон", max_length=40, blank=True, help_text="Например: +971 50 123 4567")
    whatsapp_number = models.CharField(
        "WhatsApp номер", max_length=40, blank=True,
        help_text="Только цифры с кодом страны, например 971501234567",
    )
    whatsapp_text = models.CharField(
        "Текст сообщения WhatsApp по умолчанию", max_length=200, blank=True,
        help_text="Подставляется при нажатии на кнопку WhatsApp. К нему автоматически добавляется название страницы.",
    )
    email = models.EmailField("Email", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    service_area = models.CharField("Зона обслуживания", max_length=120, blank=True, help_text="Например: Dubai & UAE")
    working_hours = models.CharField("Часы работы", max_length=120, blank=True)
    address = models.CharField("Адрес (если есть)", max_length=200, blank=True)

    notify_emails = models.CharField(
        "Email для заявок", max_length=300, blank=True,
        help_text="Куда отправлять новые заявки. Несколько адресов — через запятую.",
    )
    telegram_chat_id = models.CharField(
        "Telegram chat ID для заявок", max_length=60, blank=True,
        help_text="Необязательно. Бот присылает каждую новую заявку в Telegram.",
    )

    logo = models.FileField("Логотип (SVG или PNG)", upload_to="brand/", blank=True)
    default_og_image = models.ImageField("OG картинка по умолчанию", upload_to="og/", blank=True)
    default_seo_title = models.CharField("SEO Title по умолчанию", max_length=70, blank=True)
    default_seo_description = models.CharField("Meta Description по умолчанию", max_length=170, blank=True)

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"

    def get_absolute_url(self):
        return settings.SITE_URL + "/"


class HomePage(Singleton, SEOFields, TimeStamped):
    # Hero
    hero_eyebrow = models.CharField("Hero: надзаголовок", max_length=120, blank=True)
    hero_title = models.CharField("Hero: заголовок (H1)", max_length=160)
    hero_subtitle = models.TextField("Hero: подзаголовок", blank=True)
    hero_image = models.ImageField("Hero: фото", upload_to="home/", blank=True)
    hero_video = models.FileField(
        "Hero: видео (необязательно)", upload_to="home/", blank=True,
        help_text="MP4, без звука, до 4 МБ. Если есть — показывается вместо фото на компьютере.",
    )
    hero_cta = models.CharField("Hero: текст основной кнопки", max_length=60, blank=True)

    # About
    about_eyebrow = models.CharField("О нас: надзаголовок", max_length=80, blank=True)
    about_title = models.CharField("О нас: заголовок", max_length=200, blank=True)
    about_text = models.TextField("О нас: текст", blank=True)
    about_image = models.ImageField("О нас: фото", upload_to="home/", blank=True)

    # Directions & formats
    directions_title = models.CharField("Направления: заголовок", max_length=160, blank=True)
    formats_title = models.CharField("Форматы мероприятий: заголовок", max_length=160, blank=True)
    formats_list = models.TextField("Форматы мероприятий: список", blank=True, help_text="Каждый формат с новой строки.")

    # Packages
    packages_title = models.CharField("Пакеты: заголовок", max_length=160, blank=True)
    packages_text = models.TextField("Пакеты: текст", blank=True)

    # We work — you relax
    relax_eyebrow = models.CharField("«Мы работаем»: надзаголовок", max_length=80, blank=True)
    relax_title = models.CharField("«Мы работаем — вы отдыхаете»: заголовок", max_length=160, blank=True)
    relax_text = models.TextField("«Мы работаем»: текст", blank=True)
    relax_image = models.ImageField("«Мы работаем»: фото", upload_to="home/", blank=True)

    # Additional services
    services_title = models.CharField("Доп. услуги: заголовок", max_length=160, blank=True)
    services_text = models.TextField("Доп. услуги: текст", blank=True)
    services_note = models.CharField(
        "Доп. услуги: примечание", max_length=240, blank=True,
        help_text="Например: «Часть услуг — вместе с проверенными партнёрами».",
    )

    portfolio_title = models.CharField("Портфолио: заголовок", max_length=160, blank=True)
    portfolio_text = models.TextField("Портфолио: текст", blank=True)
    why_title = models.CharField("Почему Rokate: заголовок", max_length=160, blank=True)
    faq_title = models.CharField("FAQ: заголовок", max_length=160, blank=True)
    form_title = models.CharField("Форма: заголовок", max_length=160, blank=True)
    form_text = models.TextField("Форма: текст", blank=True)

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"

    def __str__(self):
        return "Главная страница"

    def get_absolute_url(self):
        return settings.SITE_URL + "/"


class HomeStat(models.Model):
    home = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="stats")
    value = models.CharField("Значение", max_length=20, help_text="Например: 300+")
    label = models.CharField("Подпись", max_length=80)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Цифра"
        verbose_name_plural = "Цифры (блок «О нас»)"

    def __str__(self):
        return f"{self.value} {self.label}"


class HomeStep(models.Model):
    home = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="steps")
    title = models.CharField("Заголовок", max_length=120)
    text = models.TextField("Текст", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги «Мы работаем — вы отдыхаете»"

    def __str__(self):
        return self.title


class WhyUsItem(models.Model):
    home = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="why_items")
    icon = models.CharField("Иконка", max_length=20, choices=ICON_CHOICES, default="star")
    title = models.CharField("Заголовок", max_length=120)
    text = models.TextField("Текст", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Преимущество"
        verbose_name_plural = "Почему Rokate"

    def __str__(self):
        return self.title


class AdditionalService(Publishable, TimeStamped):
    PROVIDERS = [("own", "Rokate"), ("partner", "Партнёр")]
    title = models.CharField("Название", max_length=120)
    description = models.CharField("Короткое описание", max_length=240, blank=True)
    icon = models.CharField("Иконка", max_length=20, choices=ICON_CHOICES, default="sparkle")
    provider = models.CharField(
        "Кто выполняет", max_length=10, choices=PROVIDERS, default="own",
        help_text="Только для вас — на сайте не показывается.",
    )

    class Meta(Publishable.Meta):
        verbose_name = "Дополнительная услуга"
        verbose_name_plural = "Дополнительные услуги"

    def __str__(self):
        return self.title


class FAQItem(Publishable, TimeStamped):
    PLACEMENTS = [("home", "Главная"), ("service", "Страница услуги"), ("partners", "Партнёрам")]
    question = models.CharField("Вопрос", max_length=240)
    answer = models.TextField("Ответ")
    placement = models.CharField("Где показывать", max_length=10, choices=PLACEMENTS, default="home")
    service = models.ForeignKey(
        "services.ServicePage", on_delete=models.CASCADE, null=True, blank=True,
        related_name="faq", verbose_name="Страница услуги",
    )

    class Meta(Publishable.Meta):
        verbose_name = "Вопрос FAQ"
        verbose_name_plural = "FAQ"

    def __str__(self):
        return self.question


class PartnersPage(Singleton, SEOFields, TimeStamped):
    title = models.CharField("Заголовок", max_length=160, default="Partner with Rokate")
    intro = models.TextField("Вступление", blank=True)
    audience_title = models.CharField("Для кого: заголовок", max_length=160, blank=True)
    audience = models.TextField("Для кого: список", blank=True, help_text="Каждый пункт с новой строки.")
    offer_title = models.CharField("Что предлагаем: заголовок", max_length=160, blank=True)
    offer_text = models.TextField("Что предлагаем: текст", blank=True)
    image = models.ImageField("Фото", upload_to="partners/", blank=True)
    form_title = models.CharField("Форма: заголовок", max_length=160, blank=True)

    class Meta:
        verbose_name = "Страница партнёров"
        verbose_name_plural = "Страница партнёров"

    def __str__(self):
        return "Страница партнёров"

    def get_absolute_url(self):
        return settings.SITE_URL + "/partners"


class LegalPage(SEOFields, TimeStamped):
    slug = models.SlugField("Адрес (slug)", unique=True, help_text="privacy")
    title = models.CharField("Заголовок", max_length=160)
    body = models.TextField("Текст", help_text="Абзацы разделяйте пустой строкой. Заголовок абзаца — строка, начинающаяся с ##")

    class Meta:
        verbose_name = "Юридическая страница"
        verbose_name_plural = "Юридические страницы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"{settings.SITE_URL}/{self.slug}"
