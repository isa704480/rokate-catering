"""Frontend admin (/admin) uchun resurslar ro'yxati.

Har bir resurs: qaysi model, sarlavha (rus tilida — Roman uchun), menyudagi guruh, ro'yxat ustunlari,
qidiruv, filtrlar, formadagi tablar va ichki ro'yxatlar (galereya, qadamlar...).
Formaning maydon turlari modeldan avtomatik aniqlanadi (schema.py).
"""
from apps.catering.models import CateringPackage, MenuCategory, MenuFile, MenuItem, PackageImage, SeasonalOffer
from apps.core.models import (AdditionalService, FAQItem, HomePage, HomeStat, HomeStep, LegalPage, PartnersPage,
                              SiteSettings, WhyUsItem)
from apps.leads.models import Inquiry, PartnerRequest
from apps.portfolio.models import PortfolioImage, PortfolioProject
from apps.services.models import EventType, ServiceOption, ServicePage

SEO = ["seo_title", "seo_description", "og_image", "noindex"]

RESOURCES = {
    # ---------------- Заявки ----------------
    "inquiries": dict(
        model=Inquiry, title="Заявки клиентов", one="Заявка", group="Заявки", icon="inbox",
        list=["created_at", "name", "phone", "event_type", "guests", "event_date", "source", "status"],
        search=["name", "phone", "comment"], filters=["status"],
        tabs=[("Заявка", ["status", "manager_note"]),],
        readonly=["created_at", "name", "phone", "event_date", "event_type", "guests", "location_type", "package",
                  "comment", "language", "source_page", "utm_source", "utm_medium", "utm_campaign", "referrer"],
        can_add=False, export=True, badge="new",
    ),
    "partner-requests": dict(
        model=PartnerRequest, title="Заявки партнёров", one="Заявка партнёра", group="Заявки", icon="handshake",
        list=["created_at", "name", "company", "field", "phone", "email", "status"],
        search=["name", "company", "email", "phone"], filters=["status"],
        tabs=[("Заявка", ["status", "manager_note"])],
        readonly=["created_at", "name", "company", "field", "phone", "email", "message", "language"],
        can_add=False, export=True, badge="new",
    ),

    # ---------------- Сайт ----------------
    "settings": dict(
        model=SiteSettings, title="Контакты и настройки", group="Сайт", icon="settings", singleton=True,
        tabs=[
            ("Контакты", ["company_name", "phone", "whatsapp_number", "whatsapp_text", "email", "instagram_url",
                          "service_area", "working_hours", "address", "tagline", "logo"]),
            ("Уведомления о заявках", ["notify_emails", "telegram_chat_id"]),
            ("SEO по умолчанию", ["default_seo_title", "default_seo_description", "default_og_image"]),
        ],
    ),
    "home": dict(
        model=HomePage, title="Главная страница", group="Сайт", icon="home", singleton=True,
        tabs=[
            ("Первый экран", ["hero_eyebrow", "hero_title", "hero_subtitle", "hero_cta", "hero_image", "hero_video"]),
            ("О нас", ["about_eyebrow", "about_title", "about_text", "about_image", "@stats"]),
            ("Направления и пакеты", ["directions_title", "formats_title", "formats_list", "packages_title", "packages_text"]),
            ("Мы работаем — вы отдыхаете", ["relax_eyebrow", "relax_title", "relax_text", "relax_image", "@steps"]),
            ("Доп. услуги", ["services_title", "services_text", "services_note"]),
            ("Портфолио, FAQ, форма", ["portfolio_title", "portfolio_text", "why_title", "@why_items", "faq_title",
                                       "form_title", "form_text"]),
            ("SEO", SEO),
        ],
        children={
            "stats": dict(model=HomeStat, title="Цифры", fields=["value", "label"]),
            "steps": dict(model=HomeStep, title="Шаги", fields=["title", "text"]),
            "why_items": dict(model=WhyUsItem, title="Почему Rokate", fields=["icon", "title", "text"]),
        },
    ),
    "partners-page": dict(
        model=PartnersPage, title="Страница партнёров", group="Сайт", icon="users", singleton=True,
        tabs=[("Текст", ["title", "intro", "audience_title", "audience", "offer_title", "offer_text", "form_title", "image"]),
              ("SEO", SEO)],
    ),
    "faq": dict(
        model=FAQItem, title="Вопросы и ответы (FAQ)", one="Вопрос", group="Сайт", icon="help",
        list=["question", "placement", "is_published"], search=["question_en", "question_ru"], filters=["placement"],
        tabs=[("Вопрос", ["question", "answer", "placement", "service", "is_published"])],
    ),
    "legal": dict(
        model=LegalPage, title="Политика конфиденциальности", one="Страница", group="Сайт", icon="file",
        list=["title", "slug", "updated_at"],
        tabs=[("Текст", ["slug", "title", "body"]), ("SEO", SEO)],
    ),

    # ---------------- Кейтеринг ----------------
    "packages": dict(
        model=CateringPackage, title="Готовые пакеты", one="Пакет", group="Кейтеринг", icon="gift",
        list=["image", "name", "guests_min", "guests_max", "price_from", "is_featured", "is_published"],
        search=["name_en", "name_ru"],
        tabs=[("Пакет", ["name", "slug", "image", "short_text", "contents", "guests_min", "guests_max", "price_from",
                         "price_note", "badge", "is_featured", "is_published", "@images"]),
              ("SEO", SEO)],
        children={"images": dict(model=PackageImage, title="Дополнительные фото", fields=["image", "alt"], upload="image")},
        slug_from="name",
    ),
    "offers": dict(
        model=SeasonalOffer, title="Сезонные предложения", one="Предложение", group="Кейтеринг", icon="tag",
        list=["image", "title", "starts_at", "ends_at", "is_published"],
        tabs=[("Предложение", ["title", "text", "image", "price", "starts_at", "ends_at", "cta_text", "package", "is_published"])],
    ),
    "services": dict(
        model=ServicePage, title="Направления / услуги", one="Направление", group="Кейтеринг", icon="yacht",
        list=["hero_image", "title", "slug", "show_on_home", "has_page", "is_published"],
        tabs=[("Карточка", ["title", "slug", "card_text", "hero_image", "location_type", "show_on_home", "has_page", "is_published"]),
              ("Страница", ["headline", "intro", "body", "@options", "packages", "projects"]),
              ("SEO", SEO)],
        children={"options": dict(model=ServiceOption, title="Варианты обслуживания", fields=["title", "text"])},
        slug_from="title",
    ),
    "menu": dict(
        model=MenuCategory, title="Меню", one="Категория", group="Кейтеринг", icon="book",
        list=["name", "items_count", "is_published"],
        tabs=[("Категория", ["name", "is_published", "@items"])],
        children={"items": dict(model=MenuItem, title="Позиции", fields=["name", "description", "price", "is_available", "is_published"])},
    ),
    "menu-file": dict(
        model=MenuFile, title="Меню: PDF", group="Кейтеринг", icon="pdf", singleton=True,
        tabs=[("PDF меню", ["intro", "pdf_en", "pdf_ru"])],
    ),
    "extras": dict(
        model=AdditionalService, title="Дополнительные услуги", one="Услуга", group="Кейтеринг", icon="sparkle",
        list=["icon", "title", "provider", "is_published"],
        tabs=[("Услуга", ["title", "description", "icon", "provider", "is_published"])],
    ),
    "event-types": dict(
        model=EventType, title="Типы мероприятий", one="Тип", group="Кейтеринг", icon="calendar",
        list=["name", "slug", "is_published"],
        tabs=[("Тип", ["name", "slug", "is_published"])], slug_from="name",
    ),

    # ---------------- Портфолио ----------------
    "portfolio": dict(
        model=PortfolioProject, title="Портфолио", one="Проект", group="Портфолио", icon="photo",
        list=["cover", "title", "location_type", "event_type", "photos", "is_featured", "is_published"],
        search=["title_en", "title_ru"], filters=["location_type"],
        tabs=[("Проект", ["title", "slug", "cover", "location_type", "event_type", "event_date", "guests", "description",
                          "video_url", "is_featured", "is_published"]),
              ("Галерея", ["@images"]),
              ("SEO", SEO)],
        children={"images": dict(model=PortfolioImage, title="Галерея", fields=["image", "alt"], upload="image")},
        slug_from="title",
    ),
}

GROUPS = ["Заявки", "Сайт", "Кейтеринг", "Портфолио"]
