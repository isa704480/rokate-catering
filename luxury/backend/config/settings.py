"""Rokate Catering — Django settings.

Barcha sozlamalar environment o'zgaruvchilaridan olinadi (.env.example ga qarang).
Lokal ishlab chiqishda DATABASE_URL berilmasa SQLite ishlatiladi.
"""
import os
from pathlib import Path

import dj_database_url
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


def env(name, default=None):
    return os.environ.get(name, default)


def env_bool(name, default=False):
    return str(env(name, str(default))).lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    return [x.strip() for x in env(name, default).split(",") if x.strip()]


SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-insecure-change-me")
DEBUG = env_bool("DJANGO_DEBUG", True)
if not DEBUG and SECRET_KEY.startswith("dev-insecure"):
    raise RuntimeError("Production'da DJANGO_SECRET_KEY berilishi shart")
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,backend")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", "http://localhost:3001,http://127.0.0.1:3001,http://localhost:8001")

# Admin panel manzili (maxfiy yo'l). Masalan: "manage-rk/"
ADMIN_URL = env("ADMIN_URL", "manage-rk/")

# Sayt manzili (havolalar, "View on site" uchun) va Next.js revalidate webhook
SITE_URL = env("SITE_URL", "http://localhost:3001").rstrip("/")
REVALIDATE_URL = env("REVALIDATE_URL", "http://localhost:3001/api/revalidate" if DEBUG else "")  # masalan: http://frontend:3000/api/revalidate
REVALIDATE_SECRET = env("REVALIDATE_SECRET", "dev-secret" if DEBUG else "")

# Bildirishnomalar
TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = env("TELEGRAM_CHAT_ID", "")  # SiteSettings'dagi qiymat ustun turadi
TURNSTILE_SECRET_KEY = env("TURNSTILE_SECRET_KEY", "")

INSTALLED_APPS = [
    "modeltranslation",  # admin'dan oldin bo'lishi shart
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.core",
    "apps.services",
    "apps.catering",
    "apps.portfolio",
    "apps.leads",
    "apps.panel",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Tillar ---------------------------------------------------------------
# Admin interfeysi rus tilida (Roman uchun). Sayt kontenti: EN (asosiy) + RU.
LANGUAGE_CODE = "ru"
LANGUAGES = [("en", "English"), ("ru", "Русский")]
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = ("en", "ru")
MODELTRANSLATION_FALLBACK_LANGUAGES = ("en",)
TIME_ZONE = "Asia/Dubai"
USE_I18N = True
USE_TZ = True

# --- Static / media -------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(env("MEDIA_ROOT", BASE_DIR / "media"))
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 30 * 1024 * 1024

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Email ----------------------------------------------------------------
EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", "")
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "Rokate Website <no-reply@localhost>")

# --- DRF ------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "UNAUTHENTICATED_USER": None,
}

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# Frontend admin (/admin) sessiyasi
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14  # 2 hafta
# Har variant o'z cookie nomiga ega — localhost'da 3 ta variant bir-biriga xalaqit bermaydi
SESSION_COOKIE_NAME = "rk_el_sessionid"
CSRF_COOKIE_NAME = "rk_el_csrftoken"
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# --- Xavfsizlik (production) ---------------------------------------------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "SAMEORIGIN"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# --- Unfold (admin dizayni) ----------------------------------------------
UNFOLD = {
    "SITE_TITLE": "Rokate — админ",
    "SITE_HEADER": "Rokate Catering",
    "SITE_SUBHEADER": "Управление сайтом",
    "SITE_URL": SITE_URL,
    "SITE_SYMBOL": "restaurant",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "DASHBOARD_CALLBACK": "apps.core.dashboard.dashboard_callback",
    "COLORS": {
        # Brend yashil rangi (#2D5B51) asosida
        "primary": {
            "50": "oklch(97% .015 170)",
            "100": "oklch(93% .03 170)",
            "200": "oklch(86% .05 170)",
            "300": "oklch(76% .07 170)",
            "400": "oklch(63% .08 170)",
            "500": "oklch(52% .075 170)",
            "600": "oklch(45% .065 170)",
            "700": "oklch(40% .055 170)",
            "800": "oklch(34% .045 170)",
            "900": "oklch(28% .035 170)",
            "950": "oklch(20% .025 170)",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Заявки"),
                "items": [
                    {"title": _("Панель"), "icon": "dashboard", "link": reverse_lazy("admin:index")},
                    {"title": _("Заявки клиентов"), "icon": "inbox", "link": reverse_lazy("admin:leads_inquiry_changelist"),
                     "badge": "apps.leads.admin.new_inquiries_badge"},
                    {"title": _("Заявки партнёров"), "icon": "handshake", "link": reverse_lazy("admin:leads_partnerrequest_changelist"),
                     "badge": "apps.leads.admin.new_partner_badge"},
                ],
            },
            {
                "title": _("Сайт"),
                "items": [
                    {"title": _("Настройки сайта"), "icon": "settings", "link": reverse_lazy("admin:core_sitesettings_changelist")},
                    {"title": _("Главная страница"), "icon": "home", "link": reverse_lazy("admin:core_homepage_changelist")},
                    {"title": _("Страница партнёров"), "icon": "groups", "link": reverse_lazy("admin:core_partnerspage_changelist")},
                    {"title": _("Юридические страницы"), "icon": "gavel", "link": reverse_lazy("admin:core_legalpage_changelist")},
                    {"title": _("FAQ"), "icon": "help", "link": reverse_lazy("admin:core_faqitem_changelist")},
                ],
            },
            {
                "title": _("Услуги и кейтеринг"),
                "items": [
                    {"title": _("Направления / страницы услуг"), "icon": "sailing", "link": reverse_lazy("admin:services_servicepage_changelist")},
                    {"title": _("Готовые пакеты"), "icon": "redeem", "link": reverse_lazy("admin:catering_cateringpackage_changelist")},
                    {"title": _("Сезонные предложения"), "icon": "local_offer", "link": reverse_lazy("admin:catering_seasonaloffer_changelist")},
                    {"title": _("Меню: категории"), "icon": "menu_book", "link": reverse_lazy("admin:catering_menucategory_changelist")},
                    {"title": _("Меню: PDF файлы"), "icon": "picture_as_pdf", "link": reverse_lazy("admin:catering_menufile_changelist")},
                    {"title": _("Дополнительные услуги"), "icon": "celebration", "link": reverse_lazy("admin:core_additionalservice_changelist")},
                    {"title": _("Типы мероприятий"), "icon": "event", "link": reverse_lazy("admin:services_eventtype_changelist")},
                ],
            },
            {
                "title": _("Портфолио"),
                "items": [
                    {"title": _("Проекты"), "icon": "photo_library", "link": reverse_lazy("admin:portfolio_portfolioproject_changelist")},
                ],
            },
            {
                "title": _("Доступ"),
                "items": [
                    {"title": _("Пользователи"), "icon": "person", "link": reverse_lazy("admin:auth_user_changelist"),
                     "permission": lambda request: request.user.is_superuser},
                    {"title": _("Группы"), "icon": "shield_person", "link": reverse_lazy("admin:auth_group_changelist"),
                     "permission": lambda request: request.user.is_superuser},
                ],
            },
        ],
    },
}
