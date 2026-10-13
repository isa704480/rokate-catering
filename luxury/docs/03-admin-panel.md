# 03 · Admin panel (CMS)

> Roman TZ'da aniq yozgan: *«хотел бы иметь возможность самостоятельно поменять фотографию, текст, меню, цену или контактную информацию без обращения к разработчику»*. Admin panel — loyihaning asosiy qismi.

## 1. Asosiy tamoyillar

- **Oddiy va xavfsiz.** Roman dizaynni buza olmaydi, faqat kontentni o'zgartiradi.
- **Ikki til yonma-yon.** Har bir matn maydonida `EN` va `RU` tablari bor. EN to'ldirilmagan bo'lsa, ogohlantirish chiqadi.
- **Rasm yuklash oson.** Drag & drop, avtomatik siqish (WebP/AVIF), 2–3 o'lchamli variantlar. Majburiy `alt` matn (SEO uchun), bo'sh qolsa nomdan avtomatik to'ldiriladi.
- **Tartib sichqoncha bilan.** Paketlar, portfolio va rasmlar drag & drop bilan joylashtiriladi.
- **Ko'rsatish / yashirish.** Har bir yozuvda `Published` bor. O'chirmasdan vaqtincha yashirish mumkin.
- **"View on site"** tugmasi bilan saqlangan narsani saytda darhol ko'rish mumkin.
- **Telefonda ham ishlaydi** (Unfold responsive). Roman arizalarni telefondan ko'ra oladi.
- **Admin interfeysi tili:** rus tili (Roman uchun qulay). Kerak bo'lsa ingliz tiliga almashtiriladi.

## 2. Admin menyusi (tuzilma)

```
📊 Dashboard
   ├─ Yangi arizalar (soni, oxirgi 5 tasi)
   ├─ Shu hafta / oy arizalari
   └─ Tezkor havolalar: + Paket, + Portfolio, + Taklif

📥 Заявки (Arizalar)
   ├─ Заявки клиентов        (Inquiry)
   └─ Заявки партнёров       (PartnerRequest)

🏠 Сайт
   ├─ Настройки сайта        (SiteSettings — yagona yozuv)
   ├─ Главная страница       (HomePage — yagona yozuv)
   ├─ Страница партнёров     (PartnersPage — yagona yozuv)
   └─ Политика конфиденциальности

🍽 Услуги и кейтеринг
   ├─ Страницы услуг         (ServicePage)
   ├─ Готовые пакеты         (CateringPackage)
   ├─ Сезонные предложения   (SeasonalOffer)
   ├─ Меню: категории/позиции + PDF
   ├─ Дополнительные услуги  (AdditionalService)
   └─ Типы мероприятий       (EventType)

📸 Портфолио
   └─ Проекты                (PortfolioProject + rasmlar)

❓ FAQ

👤 Пользователи и права   (faqat superuser)
```

## 3. Har bir bo'lim: maydonlar

### 3.1 Настройки сайта (SiteSettings, yagona)
| Maydon | Izoh |
|---|---|
| Kompaniya nomi | Rokate Catering |
| Telefon | `+971 ...` |
| WhatsApp raqami | wa.me havolalari uchun |
| WhatsApp standart xabari (EN/RU) | Masalan: "Hello! I'm interested in catering for my event" |
| Email | |
| Instagram URL | |
| Manzil / xizmat hududi (EN/RU) | "Dubai & UAE" |
| Ish vaqti | |
| Arizalar uchun emaillar | Vergul bilan bir nechta |
| Telegram chat ID | Bildirishnomalar uchun |
| Standart SEO Title / Description (EN/RU) | Fallback |
| Standart OG rasmi | WhatsApp yoki ijtimoiy tarmoqda ulashilganda chiqadi |
| Logotip (SVG/PNG) | |

### 3.2 Главная страница (HomePage, yagona)
- Hero: sarlavha, izoh (EN/RU), rasm, ixtiyoriy video (MP4 + poster), CTA matnlari
- Biz kimmiz: matn, 3–4 ta raqam (qiymat + izoh)
- "We work — you relax": sarlavha, matn, 4 ta ssenariy qadami (rasm + matn)
- Nega Rokate: 4 ta afzallik (ikon + sarlavha + matn)
- Qaysi paketlar ko'rsatiladi: avtomatik `featured` yoki qo'lda tanlash
- Qaysi portfolio loyihalari ko'rsatiladi: avtomatik yoki qo'lda
- SEO bloki

### 3.3 Страницы услуг (ServicePage)
| Maydon | Izoh |
|---|---|
| Nom (EN/RU), slug | `yacht-catering` |
| Qisqa tavsif (kartochka uchun) | |
| Hero rasm | |
| Asosiy matn (EN/RU) | Oddiy rich text: qalin, ro'yxat, havola |
| Xizmat variantlari | Inline ro'yxat: sarlavha + matn |
| Bog'langan paketlar | ko'p-ko'p tanlash |
| Bog'langan portfolio | ko'p-ko'p tanlash yoki joy turi bo'yicha avtomatik |
| FAQ | inline |
| Bosh sahifada ko'rsatish? / Tartib / Published | |
| **SEO bloki** | |

### 3.4 Готовые пакеты (CateringPackage) ⭐ eng muhim
| Maydon | Izoh |
|---|---|
| Nom (EN/RU) | "Yacht Brunch Set", "Pyramid Box"... |
| Mehmonlar soni: min, max | "10–15 guests" |
| Qisqa tavsif (EN/RU) | |
| Tarkibi (EN/RU) | Ro'yxat: har qator bitta punkt |
| Narx "от" (AED) | Bo'sh qolsa, "Price on request" chiqadi |
| Narx izohi | "per person" / "per set" |
| Rasm(lar) | 1–3 ta |
| Badge | "New", "Seasonal", "Bestseller" — ixtiyoriy |
| Qaysi xizmatlarga tegishli | yacht, villa... |
| Featured (bosh sahifada) / Tartib / Published | |
| SEO bloki | |

### 3.5 Сезонные предложения (SeasonalOffer)
Sarlavha, matn, rasm, narx (ixtiyoriy), **boshlanish va tugash sanasi** (saytda avtomatik chiqadi va yashirinadi), CTA, bog'langan paket.

### 3.6 Меню
- **MenuCategory:** nom (EN/RU), tartib
- **MenuItem:** kategoriya, nom, tavsif (EN/RU), narx (ixtiyoriy), `available`, tartib. Rasm maydoni yo'q, chunki Roman taom suratlari kerak emas degan.
- **Menu PDF:** EN va RU fayl yuklash. Saytda "Download menu" tugmasi chiqadi.

### 3.7 Дополнительные услуги (AdditionalService)
Nom (EN/RU), qisqa tavsif, ikon (ro'yxatdan tanlanadi), tartib, published.
Ichki maydon **"Kim bajaradi: Rokate / Hamkor"** faqat adminda ko'rinadi, saytda chiqmaydi. Roman uchun eslatma.

### 3.8 Портфолио (PortfolioProject)
| Maydon | Izoh |
|---|---|
| Nom (EN/RU), slug | |
| Tadbir turi | EventType |
| Joy turi | Yacht / Villa / Office / Home / Desert / Venue |
| Sana yoki yil | |
| Mehmonlar soni | ixtiyoriy |
| Tavsif (EN/RU) | |
| Muqova rasmi | |
| Galereya | Inline, bir nechta rasmni birdan yuklash, drag & drop tartib |
| Video URL / fayl | ixtiyoriy |
| Featured / Published | |
| SEO bloki | |

> Siz Romanga yozgansiz: *«В CMS можно будет создать новый проект, добавить: название; описание; тип мероприятия; локацию; фотографии; дату/год; дополнительные параметры; SEO Title; Meta Description»*. Bularning hammasi shu yerda bor.

### 3.9 Заявки клиентов (Inquiry)
- Ro'yxat: sana, ism, telefon (bosiladigan `wa.me` havola), tadbir turi, mehmonlar, sana, **holat**.
- Holatlar: 🆕 Yangi → 💬 Aloqada → ✅ Kelishildi → ❌ Rad etildi / 🗑 Spam.
- Filtrlar: holat, sana, tadbir turi, manba (UTM source).
- Har bir arizada: qaysi sahifadan kelgani, qaysi paket, til, UTM, referrer. Analitika uchun.
- Menejer izohi (ichki).
- **CSV/Excel eksport.**
- ⚠️ Bu CRM emas, faqat oddiy jurnal. Asosiy ish baribir WhatsApp'da bo'ladi.

### 3.10 Заявки партнёров (PartnerRequest)
Ism, kompaniya, soha, telefon, email, xabar, holat, izoh. Eksport.

### 3.11 FAQ
Savol va javob (EN/RU), qayerda ko'rsatiladi (bosh sahifa yoki xizmat sahifasi), tartib.

### 3.12 SEO bloki (barcha sahifa modellarida)
| Maydon | Cheklov |
|---|---|
| SEO Title (EN/RU) | ≤ 60 belgi, hisoblagich bilan |
| Meta Description (EN/RU) | ≤ 160 belgi, hisoblagich bilan |
| OG rasmi | bo'sh bo'lsa, asosiy rasm olinadi |
| noindex | ixtiyoriy |

Bo'sh qoldirilsa, nom va qisqa tavsifdan avtomatik yaratiladi.

## 4. Rollar va huquqlar

| Rol | Kim | Huquqlar |
|---|---|---|
| **Superuser** | Dasturchi (Nizomiddin) | Hammasi |
| **Owner** | Roman | Barcha kontent + arizalar + foydalanuvchilarni ko'rish. Tizim sozlamalari yo'q. |
| **Manager** (ixtiyoriy) | Rokate menejeri | Faqat arizalar: ko'rish, holat, izoh |

Hammasi uchun 2FA (Google Authenticator) va kuchli parol.

## 5. Avtomatik jarayonlar

| Hodisa | Nima bo'ladi |
|---|---|
| Kontent saqlandi | Next.js `revalidate` webhook, sahifa 1–2 soniyada yangilanadi |
| Rasm yuklandi | WebP/AVIF variantlar yaratiladi, EXIF (GPS) o'chiriladi, 2400 px dan katta bo'lsa kichraytiriladi |
| Yangi ariza | Bazaga yoziladi, Telegram va email'ga xabar boradi (ism, telefon, wa.me havola, tafsilotlar) |
| Taklif muddati tugadi | Saytda avtomatik yashiriladi |
| Har kecha | DB + media backup → R2 |

## 6. Romanga topshiriladigan narsa

- Admin panel bo'yicha **qisqa qo'llanma** (RU, skrinshotlar bilan, 2–3 sahifa): paket qo'shish, narxni o'zgartirish, portfolio qo'shish, rasm almashtirish, ariza bilan ishlash.
- Ixtiyoriy: 15–20 daqiqalik video-ko'rsatma (Loom yoki ekran yozuvi).
