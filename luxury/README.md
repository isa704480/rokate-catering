# Rokate Catering — Editorial / Luxury Catering (Direction 2)

> **Holat:** ✅ 1-bosqich kodi tayyor: sayt (Next.js, EN/RU) + **saytning o'zidagi admin panel `/admin`** (Next.js + Django API).
> Kontent — **demo** (`seed_demo`): matnlar qoralama, paket narxlari va kontaktlar bo'sh. Roman admin orqali to'ldiradi.

> **Dizayn — Direction 2: Editorial / Luxury Catering.** jurnal uslubi: qog'oz rangli fon, katta Playfair Display sarlavhalar, raqamlangan bo'limlar (01, 02…), menyu-karta ko'rinishidagi paketlar, to'rtburchak tugmalar.
> Bu papka — to'liq mustaqil loyiha (backend + frontend + admin). Uchala variant (`premium-minimal`, `editorial-luxury`, `modern-dynamic`) bir xil backend va admin panelga ega, faqat saytning tashqi ko'rinishi farq qiladi.

**Mijoz:** Roman Sabitov (Rokate Catering, Dubay) · **Byudjet:** $800 · **Ijrochi:** Nizomiddin

---

## Tarkibi

```
editorial-luxury/
├── backend/      Django 5.2 LTS — API: sayt (/api/v1/) + admin panel (/api/panel/), zaxira Django admin (/manage-rk/)
├── frontend/     Next.js 15 — sayt (EN: /, RU: /ru) + admin panel (/admin)
├── infra/        Docker Compose, Caddy (SSL), backup
└── docs/         Loyiha hujjatlari (TZ, arxitektura, dizayn, SEO, xarajatlar...)
```

## Manzillar (Editorial Luxury)

| | URL |
|---|---|
| Sayt (EN) | **http://localhost:3001** |
| Sayt (RU) | http://localhost:3001/ru |
| **Admin panel** | **http://localhost:3001/admin** |
| Backend API | http://localhost:8001/api/ |
| Zaxira Django admin (dasturchi) | http://localhost:8001/manage-rk/ |

Portlar kodda oldindan sozlangan — `.env` tahrirlash shart emas. Boshqa ikki variant boshqa portlarda ishlaydi, uchalasini bir vaqtda ochsa bo'ladi.

## Lokal ishga tushirish (Windows)

Kerak: **Python 3.12+** va **Node.js 20+**.

**Oson yo'l:** `start.bat` ni ikki marta bosing — birinchi safar hammasini o'zi o'rnatadi (bitta umumiy `rokate-catering\.venv`), keyin backend :8001 va frontend :3001 ni alohida oynalarda ochadi. Admin: `admin` / `admin12345`.

**Qo'lda:**

### 1. Backend (admin + API) — 1-terminal
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo          # demo kontent (rasmlar bilan)
python manage.py createsuperuser    # admin login/parol
python manage.py runserver          # → http://localhost:8001
```

### 2. Frontend (sayt) — 2-terminal
```powershell
cd frontend
copy .env.example .env.local
npm install
npm run dev                         # → http://localhost:3001
```

Admin'da saqlangan o'zgarish saytda darhol ko'rinadi (lokal revalidate avtomatik sozlangan).

## Nima tayyor

**Admin panel `/admin`** (saytning o'zida, rus tilida, Roman uchun; telefon va kompyuterda ishlaydi) — batafsil: [docs/03-admin-panel.md](docs/03-admin-panel.md), qo'llanma: [docs/admin-qollanma-ru.md](docs/admin-qollanma-ru.md)
- Dashboard: yangi arizalar, 7/30 kunlik statistika, tezkor tugmalar
- Arizalar (mijoz / hamkor): holatlar, WhatsApp havola, manba (UTM), CSV eksport, menyuda yangi arizalar soni
- Sayt sozlamalari, Bosh sahifa (barcha bloklar), Hamkorlar sahifasi, Maxfiylik siyosati, FAQ
- Xizmat yo'nalishlari / sahifalari (yangi sahifani Roman o'zi qo'shadi), Paketlar, Mavsumiy takliflar (sana bo'yicha avto chiqadi/yashirinadi), Menyu + PDF, Qo'shimcha xizmatlar, Tadbir turlari
- Portfolio: **bir nechta rasmni birdan yuklash** (iPhone HEIC ham), drag & drop tartib
- Har bir matn EN | RU yonma-yon, SEO tab (Title, Description, OG rasm, noindex), ro'yxatda «ko'rsatish» tugmalari va ↑↓ tartib
- Kirish: login/parol (Django sessiyasi, httpOnly cookie + CSRF), parolni o'zgartirish sahifasi
- Rasmlar avtomatik WebP 480/960/1600/2400 px ga aylantiriladi, EXIF (GPS) o'chiriladi
- Saqlanganda sayt darhol yangilanadi (Next.js revalidate)
- Yangi ariza → Telegram bot + email

**Sayt**
- Bosh sahifa: Hero · Biz haqimizda · Yo'nalishlar · Tadbir formatlari · Paketlar (+ mavsumiy taklif) · "We work — you relax" · Qo'shimcha xizmatlar · Portfolio (karusel + lightbox) · Nega Rokate · FAQ · Ariza formasi
- Sahifalar: `/catering/[slug]` (xizmat), `/menu`, `/partners`, `/privacy`, `/thank-you`
- EN (prefikssiz) + RU (`/ru`), hreflang, canonical
- Mobil: pastki panel (WhatsApp · Qo'ng'iroq · Ariza), mobile-first
- Ariza formasi: paket tanlash, UTM/referrer saqlanadi, honeypot + rate limit + (ixtiyoriy) Cloudflare Turnstile
- GA4 eventlari: `generate_lead`, `whatsapp_click`, `phone_click`, `email_click`, `package_request`, `menu_pdf_download`, `partner_lead`, `form_start`
- SEO: metadata, Open Graph, sitemap.xml, robots.txt, JSON-LD (Organization/LocalBusiness, Service, FAQPage, Breadcrumb)

## Production (VPS)

```sh
cd infra
cp .env.example .env        # DOMAIN, parollar, kalitlarni to'ldiring
docker compose up -d --build
docker compose exec backend python manage.py createsuperuser
# ixtiyoriy: docker compose exec backend python manage.py seed_demo
```
Caddy SSL'ni avtomatik oladi. Backup har kecha (`infra/backup`), tiklash: [infra/backup/restore.md](infra/backup/restore.md).
Xarajatlar va texnik xizmat: [docs/08-infratuzilma-va-xarajatlar.md](docs/08-infratuzilma-va-xarajatlar.md).

## Hujjatlar

| # | Fayl | Nima haqida |
|---|------|-------------|
| 00 | [docs/00-TZ-xulosa.md](docs/00-TZ-xulosa.md) | TZ xulosasi, kelishilgan qarorlar, ochiq savollar |
| 01 | [docs/01-arxitektura.md](docs/01-arxitektura.md) | Texnologiyalar, arxitektura, ADR |
| 02 | [docs/02-sahifalar-va-tuzilma.md](docs/02-sahifalar-va-tuzilma.md) | Sitemap, bloklar |
| 03 | [docs/03-admin-panel.md](docs/03-admin-panel.md) | Admin panel |
| 04 | [docs/04-malumotlar-bazasi.md](docs/04-malumotlar-bazasi.md) | DB sxemasi |
| 05 | [docs/05-api.md](docs/05-api.md) | API |
| 06 | [docs/06-dizayn.md](docs/06-dizayn.md) | Dizayn tizimi, 3 yo'nalish |
| 07 | [docs/07-seo-analitika.md](docs/07-seo-analitika.md) | SEO va analitika |
| 08 | [docs/08-infratuzilma-va-xarajatlar.md](docs/08-infratuzilma-va-xarajatlar.md) | Server, backup, yillik xarajat |
| 09 | [docs/09-reja-va-bosqichlar.md](docs/09-reja-va-bosqichlar.md) | Reja va topshirish |
| 10 | [docs/10-kontent-va-materiallar.md](docs/10-kontent-va-materiallar.md) | Materiallar inventari |
| — | [docs/admin-qollanma-ru.md](docs/admin-qollanma-ru.md) | Roman uchun admin qo'llanma (RU) |

## Keyingi qadamlar

1. Romandan: kontaktlar (telefon, WhatsApp, email, Instagram), paketlar va narxlar, menyu (PDF), vektor logotip, videolar, AI-ga o'xshash rasmlar bo'yicha javob ([docs/00](docs/00-TZ-xulosa.md#6-romanga-beriladigan-ochiq-savollar-)).
2. Roman 3 ta variantdan birini tanlaydi — tanlangani production'ga chiqariladi.
3. Domen + VPS (Roman akkauntlarida), deploy, GA4 / Search Console.
4. Cookie banner (GA4 Consent), `llms.txt`, Google Business Profile (tavsiya).
