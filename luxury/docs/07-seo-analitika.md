# 07 · SEO, GEO va analitika

## 1. Texnik SEO (Romanga va'da qilingan ro'yxat)

- [ ] Toza URL tuzilmasi, `/ru/` prefiksi, hreflang (en, ru, x-default)
- [ ] Har sahifada noyob Title va Meta Description (admindan boshqariladi)
- [ ] To'g'ri H1–H3 ierarxiyasi (sahifada bitta H1)
- [ ] `sitemap.xml` (avtomatik, ikki tilda) va `robots.txt`
- [ ] `canonical` teglar
- [ ] Open Graph + Twitter Card (WhatsApp va Instagram'da chiroyli preview)
- [ ] Rasmlar: WebP/AVIF, `srcset`, `width`/`height`, lazy-load, `alt`
- [ ] Tezlik: LCP < 2.5 s, CLS < 0.1, INP < 200 ms (mobil). Lighthouse ≥ 90
- [ ] Google Search Console (domen orqali tasdiqlash) + sitemap yuborish
- [ ] Google Analytics 4
- [ ] Dubai/UAE mahalliy qidiruvga moslashtirilgan kontent va tuzilma
- [ ] Asosiy sahifalar indeksatsiyasi tekshiriladi
- [ ] 404 sahifa, 301 redirektlar (keyinchalik slug o'zgarsa)

> Romanga aytilgan: SEO Google'da aniq o'rinni kafolatlamaydi. Natija kontent, raqobat, havolalar va keyingi ishga bog'liq.

## 2. Kalit so'zlar (boshlang'ich gipoteza)

Yakuniy ro'yxat Google Keyword Planner yoki Search Console ma'lumotlari bilan aniqlanadi.

| Sahifa | EN asosiy so'rovlar | RU |
|---|---|---|
| Bosh sahifa | catering Dubai, event catering Dubai, premium catering UAE | кейтеринг Дубай |
| Yacht | yacht catering Dubai, catering for yacht party, Dubai Marina yacht catering | кейтеринг на яхту Дубай |
| Private / Villa | villa party catering Dubai, birthday catering Dubai, private chef party Dubai | кейтеринг на день рождения Дубай |
| Corporate | corporate catering Dubai, office catering Dubai, business breakfast catering | корпоративный кейтеринг Дубай |
| Packages | catering packages Dubai, canapé platters delivery Dubai | — |

## 3. Strukturalangan ma'lumot (schema.org, JSON-LD)

| Sahifa | Schema |
|---|---|
| Barcha sahifalar | `Organization` (name, logo, sameAs: Instagram), `WebSite` |
| Bosh sahifa / Kontakt | `LocalBusiness` (telephone, areaServed: Dubai/UAE, openingHours, priceRange) |
| Xizmat sahifalari | `Service` (serviceType, provider, areaServed) + `BreadcrumbList` |
| Paketlar | `Offer` / `Product` (narx bo'lsa, `priceCurrency: AED`) |
| FAQ bloklari | `FAQPage` |
| Portfolio | `ImageGallery` / `CreativeWork` + `BreadcrumbList` |

## 4. GEO / AI Search optimizatsiyasi

Maqsad: ChatGPT, Perplexity, Google AI Overviews kabi tizimlar Rokate'ni to'g'ri "tushunishi". Siz Romanga yozgandek, bu kafolat emas.

- Aniq faktik matnlar: kim, qayerda, qanday tadbirlar, qancha mehmon, qaysi joylar.
- FAQ bloklari: odamlar beradigan savollar ("Can you cater on a yacht in Dubai Marina?").
- Schema.org (yuqorida).
- `llms.txt` fayli: kompaniya va sahifalar haqida qisqa ma'lumot (ixtiyoriy, arzon).
- Doimiy NAP (nom, manzil, telefon) sayt, Google Business Profile va Instagram'da bir xil bo'lishi.

## 5. Analitika va konversiyalar

**GA4** + **Search Console**. Ixtiyoriy: **Microsoft Clarity** (bepul, sessiya yozuvlari va heatmap).

### Eventlar

| Event | Qachon | Konversiya? |
|---|---|---|
| `generate_lead` | Ariza formasi muvaffaqiyatli yuborildi | ✅ Asosiy |
| `whatsapp_click` | Har qanday WhatsApp tugmasi (parametr: `location` = hero / sticky / package / footer) | ✅ Asosiy |
| `phone_click` | `tel:` havola | ✅ |
| `email_click` | `mailto:` havola | — |
| `partner_lead` | Hamkorlik formasi yuborildi | ✅ |
| `package_request` | Paketdagi "Request" tugmasi (parametr: paket nomi) | — |
| `menu_pdf_download` | Menyu PDF yuklab olindi | — |
| `instagram_click` | Instagram havolasi | — |
| `form_start` | Formaning birinchi maydoni to'ldirildi | — (voronka uchun) |

### Manba (qayerdan kelgan)
- GA4 standart: organic, Instagram, direct, referral.
- **UTM havolalar** Romanga tayyorlab beriladi: Instagram bio, Instagram stories, WhatsApp status, Google Business. Masalan: `?utm_source=instagram&utm_medium=bio`.
- UTM va referrer **ariza bilan birga bazaga yoziladi**, shuning uchun admin panelda har bir arizaning manbasi ko'rinadi.
- WhatsApp havolasidagi tayyor matnda sahifa nomi bo'ladi: *"Hi! I'm interested in Yacht Catering (from website)"*. Roman WhatsApp'da ham saytdan kelgan murojaatni ajrata oladi.

### Cookie / maxfiylik
- Yengil cookie banner (BAA PDPL va xalqaro tashrif buyuruvchilar uchun), GA4 Consent Mode v2.
- Maxfiylik siyosati sahifasi.

## 6. Sayt chiqqandan keyin (narxga kirmaydi, tavsiyalar)

- **Google Business Profile** yaratish yoki to'ldirish. Mahalliy qidiruv uchun eng katta ta'sir beradi, bepul.
- Instagram postlaridan muntazam ravishda portfolio loyihalari qo'shib borish.
- Haqiqiy mijozlardan Google sharhlarini so'rash.
- Yangi xizmat sahifalari: kontent paydo bo'lganda (Desert, Corporate...).
