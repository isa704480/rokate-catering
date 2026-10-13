# 05 · API (Django → Next.js)

- Bazaviy yo'l: `/api/v1/`
- Til: `?lang=en|ru` parametri. Tarjima bo'sh bo'lsa, EN qaytariladi.
- Format: JSON. O'qish endpoint'lari ochiq va keshlanadi. Yozish faqat formalar orqali.
- Faqat `is_published=true` yozuvlar qaytariladi.

## O'qish (GET)

| Endpoint | Qaytaradi |
|---|---|
| `/settings` | SiteSettings: kontaktlar, WhatsApp, ijtimoiy tarmoqlar, standart SEO |
| `/home` | HomePage + stats, steps, why-us + featured paketlar, loyihalar, xizmat kartochkalari, qo'shimcha xizmatlar, FAQ, faol takliflar |
| `/services` | Xizmat sahifalari ro'yxati (kartochka ko'rinishi) |
| `/services/{slug}` | To'liq xizmat sahifasi + variantlar + paketlar + galereya + FAQ + SEO |
| `/packages` | Paketlar ro'yxati |
| `/packages/{slug}` | Bitta paket (ixtiyoriy alohida sahifa uchun) |
| `/offers` | Faol mavsumiy takliflar (`starts_at ≤ bugun ≤ ends_at`) |
| `/menu` | Kategoriyalar + pozitsiyalar + PDF havolalar |
| `/portfolio?location=yacht&event_type=birthday` | Loyihalar ro'yxati, filtr bilan |
| `/portfolio/{slug}` | Loyiha + galereya + SEO |
| `/event-types` | Forma select uchun |
| `/partners-page` | Hamkorlar sahifasi kontenti |
| `/legal/{slug}` | Maxfiylik siyosati |
| `/sitemap-data` | Barcha slug'lar va `updated_at` (sitemap.xml uchun) |

### Rasm obyekti
```json
{
  "src": "https://<domen>/media/portfolio/12/cover-1600.webp",
  "srcset": "...-480.webp 480w, ...-960.webp 960w, ...-1600.webp 1600w",
  "width": 1600, "height": 2133,
  "alt": "Canapés and fruit platter on a yacht in Dubai Marina",
  "blur": "data:image/webp;base64,..."
}
```

## Yozish (POST)

| Endpoint | Tana | Himoya |
|---|---|---|
| `/inquiries` | name, phone, event_date, event_type, guests, location_type, comment, package, language, source_page, utm_*, referrer, turnstile_token, website (honeypot) | Turnstile, honeypot, rate limit (IP bo'yicha 5/soat) |
| `/partner-requests` | name, company, field, phone, email, message, turnstile_token, honeypot | Xuddi shunday |

Javob `201 {"ok": true}`. Frontend foydalanuvchini `/thank-you?type=inquiry` sahifasiga o'tkazadi.

## Revalidatsiya (Django → Next.js)

```
POST https://<domen>/api/revalidate
Header: X-Revalidate-Secret: <env>
Body: { "tags": ["home", "packages", "portfolio:yacht-birthday-2026"] }
```
Django har bir model saqlanganda yoki o'chirilganda tegishli teglarni yuboradi. Next.js'da `fetch(..., { next: { tags: [...] } })` ishlatiladi.

## Kesh

- Next.js: ISR + tag bo'yicha revalidate, xavfsizlik uchun fallback `revalidate: 3600`.
- Cloudflare: HTML qisqa muddatga keshlanadi, `/media/*` va `/_next/static/*` uzoq muddatga (immutable).
- `/admin`, `/api/inquiries` keshlanmaydi.
