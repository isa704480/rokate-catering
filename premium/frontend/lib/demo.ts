/**
 * DEMO rejim — backend ulanmagan (masalan Vercel'da vaqtincha).
 * Ma'lumot lib/demo-data.json dan, rasmlar public/demo-media dan olinadi.
 * Yoqiladi: DEMO_MODE=1, yoki Vercel'da API_INTERNAL_URL berilmagan bo'lsa (next.config.ts).
 * Backend ulash: Vercel'da API_INTERNAL_URL=https://... qo'shib, qayta deploy qiling.
 */
export const DEMO = process.env.NEXT_PUBLIC_DEMO_MODE === "1";
