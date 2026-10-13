# Rokate Catering — 3 ta dizayn varianti

Dubaydagi premium katering sayti (EN + RU, admin panel). Bitta repoda 3 ta mustaqil loyiha:

| Papka | Dizayn | Lokal sayt | Lokal backend |
|---|---|---|---|
| `premium/` | Premium Minimal | http://localhost:3000 | http://localhost:8000 |
| `luxury/` | Editorial Luxury | http://localhost:3001 | http://localhost:8001 |
| `modern/` | Modern Dynamic | http://localhost:3002 | http://localhost:8002 |

Har bir papkada: `backend/` (Django + API + admin API), `frontend/` (Next.js sayt + `/admin` panel), `infra/` (Docker, Caddy), `docs/`.

## Lokal ishga tushirish (Windows)
Papka ichidagi `start.bat` — birinchi safar hammasini o'zi o'rnatadi. Admin: `admin` / `admin12345`.

## Vercel (har variant — alohida Vercel loyiha, bitta repodan)

Vercel → **Add New → Project** → shu repo → **Root Directory** ni tanlang:

| Vercel loyiha | Root Directory |
|---|---|
| rokate-premium | `premium/frontend` |
| rokate-luxury | `luxury/frontend` |
| rokate-modern | `modern/frontend` |

**Hozir (DEMO rejim):** Environment Variables shart emas. `API_INTERNAL_URL` berilmasa sayt backend'siz ishlaydi —
matn va rasmlar `frontend/lib/demo-data.json` va `frontend/public/demo-media/` dan olinadi, forma "rahmat" sahifasiga o'tadi (ariza saqlanmaydi), `/admin` "demo" xabarini ko'rsatadi.

**Backend ulanganda** — Environment Variables qo'shib, Redeploy qiling:
```
API_INTERNAL_URL=https://<shu variant backend manzili>
NEXT_PUBLIC_SITE_URL=https://<shu vercel domeni>
REVALIDATE_SECRET=<uzun tasodifiy satr — backend'dagi bilan bir xil>
```
Muhim: Vercel faqat **frontend**ni joylaydi. Django backend (baza, rasm yuklash, admin API) alohida serverda ishlashi kerak — har variantga o'z backend'i.
