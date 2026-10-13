"""Demo kontent: saytni darhol ko'rish uchun.

    python manage.py seed_demo          # bo'sh bazaga demo kontent
    python manage.py seed_demo --reset  # mavjud kontentni o'chirib, qaytadan

⚠️ Matnlar, paketlar va FAQ — QORALAMA. Roman tasdiqlashi va to'ldirishi kerak.
Paket narxlari ataylab bo'sh ("Price on request"), raqamlar (statistika) qo'shilmagan:
Romandan haqiqiy ma'lumot olinmaguncha hech narsa o'ylab topilmaydi.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from apps.catering.models import CateringPackage, MenuCategory, MenuFile, MenuItem
from apps.core.models import (AdditionalService, FAQItem, HomePage, HomeStep, LegalPage, PartnersPage,
                              SiteSettings, WhyUsItem)
from apps.portfolio.models import PortfolioImage, PortfolioProject
from apps.services.models import EventType, ServiceOption, ServicePage

IMG_DIR = Path(settings.BASE_DIR) / "seed" / "images"


def img(name):
    path = IMG_DIR / f"{name}.jpg"
    return File(path.open("rb"), name=path.name)


def setimg(obj, field, name):
    getattr(obj, field).save(f"{name}.jpg", img(name), save=False)


class Command(BaseCommand):
    help = "Demo kontentni yaratadi (EN + RU)."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Avvalgi kontentni o'chirish")

    def handle(self, *args, **opts):
        from apps.core import signals

        signals.SUSPENDED = True
        try:
            self._handle(*args, **opts)
        finally:
            signals.SUSPENDED = False
        signals.trigger_revalidate()

    def _handle(self, *args, reset=False, **opts):
        if reset:
            for m in (PortfolioProject, ServicePage, CateringPackage, MenuCategory, AdditionalService, FAQItem,
                      EventType, HomePage, PartnersPage, LegalPage, MenuFile):
                m.objects.all().delete()  # QuerySet.delete singleton'larni ham o'chiradi
        if ServicePage.objects.exists():
            self.stdout.write(self.style.WARNING("Kontent allaqachon bor. Qayta yaratish uchun: --reset"))
            return

        self.settings()
        types = self.event_types()
        projects = self.portfolio(types)
        packages = self.packages()
        self.services(packages, projects)
        self.home()
        self.extras()
        self.menu()
        self.partners()
        self.legal()
        self.stdout.write(self.style.SUCCESS("✓ Demo kontent yaratildi"))

    # ------------------------------------------------------------------
    def settings(self):
        s = SiteSettings.load()
        s.company_name = "Rokate Catering"
        s.tagline_en = "Premium catering for yachts, villas and events in Dubai."
        s.tagline_ru = "Премиальный кейтеринг для яхт, вилл и мероприятий в Дубае."
        s.whatsapp_text_en = "Hello Rokate! I'd like to plan catering for my event."
        s.whatsapp_text_ru = "Здравствуйте, Rokate! Хочу заказать кейтеринг для мероприятия."
        s.service_area_en = "Dubai, UAE"
        s.service_area_ru = "Дубай, ОАЭ"
        s.working_hours_en = "Every day, by appointment"
        s.working_hours_ru = "Ежедневно, по договорённости"
        # Kontaktlar Romandan olinadi — hozircha bo'sh (saytda tegishli tugmalar yashiriladi)
        s.default_seo_title_en = "Rokate Catering — Premium Event Catering in Dubai"
        s.default_seo_title_ru = "Rokate Catering — премиальный кейтеринг в Дубае"
        s.default_seo_description_en = ("Catering for yachts, villas, offices and private events in Dubai. "
                                        "Food, service, setup and everything around it — you just enjoy the day.")
        s.default_seo_description_ru = ("Кейтеринг на яхтах, виллах, в офисах и на частных мероприятиях в Дубае. "
                                        "Еда, сервис, оформление — а вы просто наслаждаетесь праздником.")
        s.save()

    def event_types(self):
        data = [
            ("birthday", "Birthdays", "Дни рождения"),
            ("private", "Private events", "Частные мероприятия"),
            ("corporate", "Corporate events", "Корпоративные мероприятия"),
            ("opening", "Grand openings", "Торжественные открытия"),
            ("breakfast", "Business breakfasts", "Деловые завтраки"),
            ("presentation", "Meetings & presentations", "Встречи и презентации"),
            ("reception", "Buffets & receptions", "Фуршеты и приёмы"),
            ("yacht", "Yacht parties", "Мероприятия на яхтах"),
            ("villa", "Villa parties", "Мероприятия на виллах"),
            ("other", "Other", "Другое"),
        ]
        out = {}
        for i, (slug, en, ru) in enumerate(data):
            out[slug] = EventType.objects.create(slug=slug, name_en=en, name_ru=ru, order=i)
        return out

    def portfolio(self, t):
        data = [
            ("yacht-brunch-dubai-marina", "yacht", "yacht", "yacht-deck-table",
             "Brunch on a yacht in Dubai Marina", "Бранч на яхте в Dubai Marina",
             "Canapés, fresh fruit and sparkling wine served on deck, with flowers and full table setting.",
             "Канапе, свежие фрукты и игристое на палубе — с цветами и полной сервировкой.",
             ["yacht-oysters-fruit", "platters-closeup", "waitress-fruit-platter"]),
            ("birthday-on-a-yacht", "yacht", "birthday", "yacht-birthday-balloons",
             "Birthday party on a yacht", "День рождения на яхте",
             "Balloon decor, a buffet table and service on board — the guests only had to celebrate.",
             "Оформление шарами, фуршетный стол и обслуживание на борту — гостям оставалось только праздновать.",
             ["yacht-birthday-table", "yacht-lounge-snacks"]),
            ("yacht-buffet", "yacht", "reception", "yacht-canape-buffet",
             "Buffet in the yacht salon", "Фуршет в салоне яхты",
             "Tartlets, cheese boards, fruit and hot snacks arranged in the main salon.",
             "Тарталетки, сырные доски, фрукты и горячие закуски в главном салоне.",
             ["yacht-salon-buffet", "seafood-fruit-table"]),
            ("villa-evening-dinner", "villa", "villa", "villa-dinner-night",
             "Evening dinner at a villa", "Вечерний ужин на вилле",
             "A long dinner table under string lights and palm trees, with full serving.",
             "Длинный стол под гирляндами и пальмами, с полной сервировкой.",
             ["white-table-setting"]),
            ("office-reception", "office", "corporate", "office-reception",
             "Corporate reception in an office", "Корпоративный фуршет в офисе",
             "Canapés, desserts and drinks for a corporate event with a view of the city.",
             "Канапе, десерты и напитки для корпоративного мероприятия с видом на город.",
             ["canape-marble-table"]),
            ("bbq-on-board", "yacht", "yacht", "chef-bbq-yacht",
             "BBQ on board", "BBQ на борту",
             "Our chef grills skewers, vegetables and seafood right on the yacht.",
             "Наш шеф готовит шашлычки, овощи и морепродукты прямо на яхте.",
             ["chef-grill-skewers", "chef-on-yacht"]),
            ("pyramid-box-picnic", "desert", "private", "pyramid-box-picnic",
             "Picnic with Pyramid Box", "Пикник с Pyramid Box",
             "Ready-made Pyramid Box sets for an outdoor picnic.",
             "Готовые сеты Pyramid Box для пикника на природе.",
             []),
        ]
        out = {}
        for i, (slug, loc, et, cover, ten, tru, den, dru, gallery) in enumerate(data):
            p = PortfolioProject(slug=slug, location_type=loc, event_type=t[et], title_en=ten, title_ru=tru,
                                 description_en=den, description_ru=dru, order=i)
            setimg(p, "cover", cover)
            p.save()
            for j, g in enumerate(gallery):
                pi = PortfolioImage(project=p, order=j, alt_en=ten, alt_ru=tru)
                setimg(pi, "image", g)
                pi.save()
            out[slug] = p
        return out

    def packages(self):
        data = [
            ("pyramid-box", "Pyramid Box", "Pyramid Box", "pyramid-box-picnic", 2, 6, "signature",
             "Our signature ready-made box: a beautifully packed set of snacks, perfect for picnics and gifts.",
             "Наш фирменный готовый бокс: красиво упакованный сет закусок для пикника или в подарок.",
             "Canapés and finger food\nFresh fruit\nCheese selection\nDesserts",
             "Канапе и finger food\nСвежие фрукты\nСырная нарезка\nДесерты"),
            ("yacht-brunch", "Yacht Brunch", "Бранч на яхте", "platters-closeup", 10, 20, "bestseller",
             "A balanced brunch set for a day on the water: light, fresh and beautifully served.",
             "Сбалансированный бранч для дня на воде: легко, свежо и красиво.",
             "Croissants and mini sandwiches\nCanapés with salmon\nFruit platter\nCheese board\nDesserts",
             "Круассаны и мини-сэндвичи\nКанапе с лососем\nФруктовое ассорти\nСырная доска\nДесерты"),
            ("canape-reception", "Canapé Reception", "Фуршет с канапе", "canape-marble-table", 20, 60, "",
             "Finger food and canapés for receptions, openings and corporate events.",
             "Канапе и finger food для приёмов, открытий и корпоративных мероприятий.",
             "Assorted canapés\nTartlets\nMini desserts\nFruit\nService staff on request",
             "Ассорти канапе\nТарталетки\nМини-десерты\nФрукты\nОфицианты по запросу"),
            ("bbq-on-board", "BBQ Experience", "BBQ на борту", "chef-grill-skewers", 10, 30, "",
             "Live grill with our chef — on a yacht, at a villa or outdoors.",
             "Живой гриль с нашим шефом — на яхте, на вилле или на природе.",
             "Chicken and beef skewers\nGrilled vegetables\nSeafood\nSalads and sauces\nChef on site",
             "Шашлычки из курицы и говядины\nОвощи гриль\nМорепродукты\nСалаты и соусы\nШеф на площадке"),
        ]
        out = {}
        for i, (slug, en, ru, image, gmin, gmax, badge, sen, sru, cen, cru) in enumerate(data):
            p = CateringPackage(slug=slug, name_en=en, name_ru=ru, guests_min=gmin, guests_max=gmax, badge=badge,
                                short_text_en=sen, short_text_ru=sru, contents_en=cen, contents_ru=cru,
                                price_note_en="", price_note_ru="", order=i)
            setimg(p, "image", image)
            p.save()
            out[slug] = p
        return out

    def services(self, packages, projects):
        data = [
            ("yacht-catering", "yacht", "yacht-deck-table", True,
             "Yacht Catering", "Кейтеринг на яхте",
             "Food, setup and service on board — from brunch to a full party.",
             "Еда, сервировка и обслуживание на борту — от бранча до полноценной вечеринки.",
             "Yacht Catering in Dubai", "Кейтеринг на яхте в Дубае",
             "We bring everything on board: food, tableware, decor and staff. You and your guests enjoy the sea.",
             "Мы привозим на борт всё необходимое: еду, посуду, декор и персонал. Вы с гостями наслаждаетесь морем.",
             ["yacht-brunch", "canape-reception", "bbq-on-board"],
             ["yacht-brunch-dubai-marina", "birthday-on-a-yacht", "yacht-buffet", "bbq-on-board"]),
            ("private-events", "villa", "villa-dinner-night", True,
             "Villa & Private Events", "Виллы и частные праздники",
             "Birthdays, family celebrations and dinners at a villa or at home.",
             "Дни рождения, семейные праздники и ужины на вилле или дома.",
             "Private Event Catering in Dubai", "Кейтеринг для частных мероприятий в Дубае",
             "Birthdays, anniversaries and dinners with friends — we take care of the table, service and setup.",
             "Дни рождения, юбилеи и ужины с друзьями — мы берём на себя стол, сервис и оформление.",
             ["canape-reception", "bbq-on-board"],
             ["villa-evening-dinner", "birthday-on-a-yacht"]),
            ("corporate-catering", "office", "office-reception", False,
             "Corporate & Office", "Корпоративы и офисы",
             "Receptions, business breakfasts, presentations and openings.",
             "Фуршеты, деловые завтраки, презентации и открытия.",
             "Corporate Catering in Dubai", "Корпоративный кейтеринг в Дубае", "", "",
             ["canape-reception"], ["office-reception"]),
            ("outdoor-catering", "desert", "pyramid-box-picnic", False,
             "Desert & Outdoor", "Пустыня и outdoor",
             "Picnics and outdoor events — including our Pyramid Box sets.",
             "Пикники и мероприятия на природе — в том числе с нашими сетами Pyramid Box.",
             "Outdoor Catering in Dubai", "Outdoor кейтеринг в Дубае", "", "",
             ["pyramid-box"], ["pyramid-box-picnic"]),
        ]
        for i, (slug, loc, image, has_page, ten, tru, cen, cru, hen, hru, ien, iru, pk, pr) in enumerate(data):
            sp = ServicePage(slug=slug, location_type=loc, has_page=has_page, order=i,
                             title_en=ten, title_ru=tru, card_text_en=cen, card_text_ru=cru,
                             headline_en=hen, headline_ru=hru, intro_en=ien, intro_ru=iru)
            setimg(sp, "hero_image", image)
            sp.save()
            sp.packages.set([packages[x] for x in pk])
            sp.projects.set([projects[x] for x in pr])
        yacht = ServicePage.objects.get(slug="yacht-catering")
        yacht.body_en = ("A yacht is a special venue: limited space, no kitchen on board in many cases and guests "
                         "who expect everything to look perfect. We plan the menu and logistics around the boat, "
                         "bring everything ready to serve and take care of the setup and cleaning.\n\n"
                         "Choose a ready-made package or tell us about your event — we will prepare a proposal "
                         "for your number of guests and format.")
        yacht.body_ru = ("Яхта — особая площадка: мало места, часто нет кухни на борту, а гости ждут, что всё будет "
                         "выглядеть идеально. Мы планируем меню и логистику под конкретную яхту, привозим всё готовым "
                         "к подаче, берём на себя сервировку и уборку.\n\n"
                         "Выберите готовый пакет или расскажите о мероприятии — мы подготовим предложение под ваше "
                         "количество гостей и формат.")
        yacht.save()
        opts = [("Brunch & breakfast", "Бранч и завтрак", "Light and fresh: pastries, canapés, fruit.", "Легко и свежо: выпечка, канапе, фрукты."),
                ("Buffet & canapés", "Фуршет и канапе", "Finger food for parties on board.", "Finger food для вечеринок на борту."),
                ("BBQ on board", "BBQ на борту", "Our chef grills right on the yacht.", "Шеф готовит гриль прямо на яхте."),
                ("Full service", "Полный сервис", "Staff, tableware, decor and cleaning.", "Персонал, посуда, декор и уборка.")]
        for i, (ten, tru, xen, xru) in enumerate(opts):
            ServiceOption.objects.create(service=yacht, order=i, title_en=ten, title_ru=tru, text_en=xen, text_ru=xru)
        FAQItem.objects.create(service=yacht, placement="service", order=0,
                               question_en="Can you cater on any yacht?", question_ru="Вы работаете на любой яхте?",
                               answer_en="Yes — tell us the yacht, marina and number of guests, and we will plan the menu and setup for it.",
                               answer_ru="Да — сообщите яхту, марину и количество гостей, и мы спланируем меню и сервировку под неё.")

    def home(self):
        h = HomePage.load()
        T = {
            "hero_eyebrow": ("Dubai · Yachts · Villas · Events", "Дубай · Яхты · Виллы · Мероприятия"),
            "hero_title": ("Premium catering for yachts, villas & events", "Премиальный кейтеринг для яхт, вилл и мероприятий"),
            "hero_subtitle": ("Food, service, setup and everything around it. We work — you relax and enjoy your guests.",
                              "Еда, сервис, оформление и всё, что вокруг. Мы работаем — вы отдыхаете и наслаждаетесь праздником."),
            "hero_cta": ("Get a proposal", "Получить предложение"),
            "about_eyebrow": ("About Rokate", "О Rokate"),
            "about_title": ("Not just food delivery — a fully catered event", "Не просто доставка еды — полноценное обслуживание мероприятия"),
            "about_text": ("Rokate Catering is an event catering company in Dubai. We come to your venue — a yacht, a villa, "
                           "an office or the desert — and take care of the food, serving and service.\n\n"
                           "When you need more, we help with staff, furniture, tableware, decor, a photographer or a DJ — "
                           "on our own or together with trusted partners.",
                           "Rokate Catering — кейтеринговая компания в Дубае. Мы приезжаем на вашу площадку — яхту, виллу, "
                           "в офис или в пустыню — и берём на себя еду, сервировку и обслуживание.\n\n"
                           "Если нужно больше, поможем с персоналом, мебелью, посудой, декором, фотографом или DJ — "
                           "сами или вместе с проверенными партнёрами."),
            "directions_title": ("Where we cater", "Где мы работаем"),
            "formats_title": ("Events we cater", "Форматы мероприятий"),
            "formats_list": ("Birthdays\nPrivate parties\nCorporate events\nGrand openings\nBusiness breakfasts\n"
                             "Meetings & presentations\nBuffets & receptions\nYacht parties\nVilla parties",
                             "Дни рождения\nЧастные праздники\nКорпоративы\nОткрытия\nДеловые завтраки\n"
                             "Встречи и презентации\nФуршеты и приёмы\nВечеринки на яхтах\nПраздники на виллах"),
            "packages_title": ("Ready-made catering packages", "Готовые кейтеринг-пакеты"),
            "packages_text": ("Not sure how much food you need for 20 guests? Start with a package — we will adjust it to your event.",
                              "Сложно понять, сколько еды нужно на 20 гостей? Начните с готового пакета — мы адаптируем его под ваше мероприятие."),
            "relax_eyebrow": ("Our approach", "Наш подход"),
            "relax_title": ("We work — you relax", "Мы работаем — вы отдыхаете"),
            "relax_text": ("Why search for furniture, tableware, a decorator, catering, a photographer and a DJ and coordinate "
                           "them all yourself? Leave the organisation to us and spend the time with your guests.",
                           "Зачем самому искать мебель, посуду, декоратора, кейтеринг, фотографа и DJ и координировать их между собой? "
                           "Доверьте организацию нам и проведите это время с гостями."),
            "services_title": ("Everything for your event", "Всё необходимое для мероприятия"),
            "services_text": ("One request instead of a dozen contractors. Tell us what you need — we put it together in one place.",
                              "Одно обращение вместо десятка подрядчиков. Расскажите, что нужно, — мы соберём всё в одном месте."),
            "services_note": ("Some services are provided together with our trusted partners.",
                              "Часть услуг мы оказываем вместе с проверенными партнёрами."),
            "portfolio_title": ("Our events", "Наши мероприятия"),
            "portfolio_text": ("Real events we have catered.", "Реальные мероприятия, которые мы обслуживали."),
            "why_title": ("Why Rokate", "Почему Rokate"),
            "faq_title": ("Questions & answers", "Вопросы и ответы"),
            "form_title": ("Tell us about your event", "Расскажите о вашем мероприятии"),
            "form_text": ("Leave a request and we will get back to you with a proposal. Or just message us on WhatsApp.",
                          "Оставьте заявку — мы свяжемся с вами и подготовим предложение. Или просто напишите нам в WhatsApp."),
        }
        for f, (en, ru) in T.items():
            setattr(h, f"{f}_en", en)
            setattr(h, f"{f}_ru", ru)
        setimg(h, "hero_image", "yacht-deck-table")
        setimg(h, "about_image", "chef-bbq-yacht")
        setimg(h, "relax_image", "family-on-yacht")
        h.save()
        h.steps.all().delete()
        h.why_items.all().delete()
        steps = [("We arrive and set up", "Приезжаем и готовим площадку", "Furniture, tableware, decor and flowers.", "Мебель, посуда, декор и цветы."),
                 ("We serve", "Сервируем и угощаем", "Food and drinks served beautifully and on time.", "Еда и напитки — красиво и вовремя."),
                 ("You enjoy", "Вы наслаждаетесь", "Our staff takes care of the guests, music and photos are covered.", "Персонал заботится о гостях, музыка и фото — под контролем."),
                 ("We clean up", "Убираем за собой", "After the event we take everything back. You keep only the memories.", "После мероприятия мы всё увозим. У вас остаются только впечатления.")]
        for i, (ten, tru, xen, xru) in enumerate(steps):
            HomeStep.objects.create(home=h, order=i, title_en=ten, title_ru=tru, text_en=xen, text_ru=xru)
        why = [("chef", "Catering is our core", "Кейтеринг — наш основной продукт", "Everything else is built around great food and service.", "Всё остальное строится вокруг вкусной еды и сервиса."),
               ("yacht", "Any venue", "Любая площадка", "Yachts, villas, offices, homes and outdoor locations.", "Яхты, виллы, офисы, дома и outdoor-локации."),
               ("key", "One contact for everything", "Один контакт на всё", "We coordinate staff, decor and partners for you.", "Мы координируем персонал, декор и партнёров за вас."),
               ("sparkle", "Made for your event", "Под ваше мероприятие", "Packages are a starting point — we adjust every proposal.", "Пакеты — лишь отправная точка, каждое предложение мы адаптируем.")]
        for i, (icon, ten, tru, xen, xru) in enumerate(why):
            WhyUsItem.objects.create(home=h, order=i, icon=icon, title_en=ten, title_ru=tru, text_en=xen, text_ru=xru)

    def extras(self):
        services = [("chair", "Furniture", "Мебель"), ("plate", "Tableware & serving", "Посуда и сервировка"),
                    ("sparkle", "Decor", "Декор"), ("balloon", "Balloons", "Воздушные шары"),
                    ("flower", "Flowers & floristry", "Цветы и флористика"), ("frame", "Photo zones", "Фотозоны"),
                    ("camera", "Photo & video", "Фотограф и видеограф"), ("music", "DJ", "DJ"),
                    ("villa", "Villa rental", "Аренда виллы"), ("yacht", "Yacht rental", "Аренда яхты"),
                    ("car", "Car rental", "Аренда автомобилей"), ("people", "Staff", "Персонал")]
        for i, (icon, en, ru) in enumerate(services):
            AdditionalService.objects.create(icon=icon, title_en=en, title_ru=ru, order=i,
                                             provider="own" if icon in ("plate", "people") else "partner")
        faq = [("Do you cater on yachts?", "Вы работаете на яхтах?",
                "Yes, yachts are one of our main venues. Tell us the yacht, marina and number of guests — we will plan everything for it.",
                "Да, яхты — одна из наших основных площадок. Сообщите яхту, марину и количество гостей — мы всё спланируем."),
               ("How much does catering cost?", "Сколько стоит кейтеринг?",
                "Every event is calculated individually: it depends on the number of guests, menu, staff and format. "
                "Ready-made packages are a good starting point.",
                "Каждое мероприятие рассчитывается индивидуально: всё зависит от количества гостей, меню, персонала и формата. "
                "Готовые пакеты — хорошая отправная точка."),
               ("Can you help with decor, furniture or a DJ?", "Поможете с декором, мебелью или DJ?",
                "Yes. We can organise furniture, tableware, decor, flowers, a photographer, a DJ and more — on our own or with trusted partners.",
                "Да. Мы можем организовать мебель, посуду, декор, цветы, фотографа, DJ и многое другое — сами или с проверенными партнёрами."),
               ("Can the menu be adjusted?", "Можно изменить меню?",
                "Of course. Packages are a starting point; we adjust the menu to your guests, preferences and dietary needs.",
                "Конечно. Пакеты — это отправная точка; мы адаптируем меню под ваших гостей, предпочтения и ограничения в питании."),
               ("How do I place an order?", "Как оформить заказ?",
                "Leave a request on the website or message us on WhatsApp with the date, venue and number of guests. We will reply with a proposal.",
                "Оставьте заявку на сайте или напишите в WhatsApp: дата, площадка и количество гостей. Мы ответим с предложением.")]
        for i, (qen, qru, aen, aru) in enumerate(faq):
            FAQItem.objects.create(placement="home", order=i, question_en=qen, question_ru=qru, answer_en=aen, answer_ru=aru)

    def menu(self):
        mf = MenuFile.load()
        mf.intro_en = "A selection from our menu. Not sure what to choose? Start with a ready-made package or ask us on WhatsApp."
        mf.intro_ru = "Позиции из нашего меню. Сложно выбрать? Начните с готового пакета или спросите нас в WhatsApp."
        mf.save()
        cats = [("Canapés & finger food", "Канапе и finger food",
                 [("Salmon canapés", "Канапе с лососем"), ("Caviar tartlets", "Тарталетки с икрой"), ("Mini croissants", "Мини-круассаны")]),
                ("Platters", "Ассорти",
                 [("Fruit platter", "Фруктовое ассорти"), ("Cheese board", "Сырная доска"), ("Seafood platter", "Ассорти из морепродуктов")]),
                ("BBQ", "BBQ", [("Chicken skewers", "Шашлычки из курицы"), ("Grilled vegetables", "Овощи гриль")]),
                ("Desserts", "Десерты", [("Mini desserts", "Мини-десерты")])]
        for i, (cen, cru, items) in enumerate(cats):
            c = MenuCategory.objects.create(name_en=cen, name_ru=cru, order=i)
            for j, (ien, iru) in enumerate(items):
                MenuItem.objects.create(category=c, name_en=ien, name_ru=iru, order=j)

    def partners(self):
        p = PartnersPage.load()
        p.title_en, p.title_ru = "Partner with Rokate", "Партнёрам Rokate"
        p.intro_en = ("We are open to long-term cooperation with companies and specialists who need a reliable catering "
                      "partner for their clients or their own events.")
        p.intro_ru = ("Мы открыты к сотрудничеству с компаниями и специалистами, которым нужен надёжный кейтеринговый "
                      "партнёр для своих клиентов или собственных мероприятий.")
        p.audience_title_en, p.audience_title_ru = "Who we work with", "С кем мы работаем"
        p.audience_en = ("Yacht companies & brokers\nEvent agencies\nConcierge services\nReal estate professionals\n"
                         "Luxury & service companies")
        p.audience_ru = ("Яхтенные компании и брокеры\nEvent-агентства\nConcierge-компании\nСпециалисты по недвижимости\n"
                         "Компании из luxury/service сегмента")
        p.offer_title_en, p.offer_title_ru = "What we offer", "Что мы предлагаем"
        p.offer_text_en = "Individual B2B terms and different cooperation formats. Leave a request — we will discuss the details personally."
        p.offer_text_ru = "Индивидуальные B2B-условия и разные форматы сотрудничества. Оставьте заявку — детали обсудим лично."
        p.form_title_en, p.form_title_ru = "Become a partner", "Стать партнёром"
        setimg(p, "image", "yacht-salon-buffet")
        p.save()

    def legal(self):
        LegalPage.objects.create(
            slug="privacy",
            title_en="Privacy Policy", title_ru="Политика конфиденциальности",
            body_en=("## What we collect\nWhen you send a request, we receive your name, phone number and the event details "
                     "you provide.\n\n## Why\nOnly to contact you and prepare a proposal.\n\n## Analytics\nWe use Google "
                     "Analytics to understand how the website is used.\n\n## Contact\nTo update or delete your data, contact us "
                     "via WhatsApp or email.\n\n*Draft — to be reviewed by Rokate before launch.*"),
            body_ru=("## Какие данные мы получаем\nКогда вы отправляете заявку, мы получаем ваше имя, телефон и детали "
                     "мероприятия.\n\n## Зачем\nТолько чтобы связаться с вами и подготовить предложение.\n\n## Аналитика\n"
                     "Мы используем Google Analytics, чтобы понимать, как используется сайт.\n\n## Связь\nЧтобы изменить или "
                     "удалить данные, напишите нам в WhatsApp или на email.\n\n*Черновик — Rokate проверит перед запуском.*"),
        )
