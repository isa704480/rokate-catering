# 06 · Dizayn

## 1. Romanning talablari (iqtibos)

- *«современно, премиально, чисто, визуально дорого, но без излишнего пафоса»*
- Sayt **quyidagilarga o'xshamasligi kerak:** oddiy ovqat yetkazib berish, internet-do'kon, arzon ommaviy katering, haddan tashqari bezatilgan luxury sayt.
- *«светлая и нейтральная основа»*, aksentlar firma ranglarida: yashil, oltin, oq.
- Laym rangi faqat aksent sifatida. Butun dizayn yorqin laym fonida qurilmaydi.
- **Sifatli fotosuratlar asosiy rolni o'ynaydi.**
- Animatsiyalar me'yorida, saytni ular bilan to'ldirmaslik kerak.

## 2. Brend aktivlari (arxivdan)

Rokate'da ikki xil brend ko'rinishi bor:

| Variant | Qayerda | Ranglar (rasmdan olingan, taxminiy) |
|---|---|---|
| **A. Laym** | Instagram avatar, logo | fon `#D2DD2B` (laym), yozuv `#152040` (to'q ko'k-siyoh) |
| **B. Oq qadoq** | Pyramid Box | oq fon, yozuv `≈#2D5B51` (to'q yashil), yoy `≈ bej-oltin` |

Logotip qo'lda yozilgan shriftda: "Rokate", aylana yoy va "CATERING". **Vektor fayl kerak** (Romandan so'raladi). Saytda B varianti asos qilib olinadi, chunki Roman yashil va oltinni so'ragan. Laym kichik aksentlarda ishlatiladi.

## 3. Design tokens (taklif)

```css
/* Asosiy palitra — barcha yo'nalishlar uchun umumiy */
--color-bg:          #FAF8F3;  /* iliq oq / ivory */
--color-surface:     #FFFFFF;
--color-sand:        #F1ECE2;  /* bloklarni ajratish uchun */
--color-ink:         #152040;  /* asosiy matn — logodagi to'q ko'k */
--color-ink-muted:   #5B6275;
--color-green:       #2D5B51;  /* brend yashil (Pyramid Box logosi) */
--color-green-deep:  #1F433B;  /* hover / footer foni */
--color-gold:        #B89B5E;  /* oltin aksent: chiziqlar, ikonlar, badge */
--color-lime:        #D2DD2B;  /* NUQTAVIY: kichik belgi, hover underline, badge */
--color-line:        #E4DED2;

--radius-sm: 6px;  --radius-md: 12px;  --radius-lg: 20px;
--shadow-card: 0 8px 30px rgba(21,32,64,.06);
```

Kontrast: `ink` `bg` ustida AA talabidan ancha yuqori. Laym rang hech qachon oq ustidagi matn uchun ishlatilmaydi (kontrast past).

**CTA tugmalari:** asosiy tugma `green`, oq matn bilan. WhatsApp tugmasi alohida, WhatsApp yashili (`#25D366`) faqat ikonda. Ikkilamchi tugma: ingichka `ink` chegarali.

## 4. Shriftlar (kirill alifbosini qo'llab-quvvatlashi shart)

| Yo'nalish | Sarlavhalar | Asosiy matn |
|---|---|---|
| Premium Minimal | Cormorant Garamond (500/600) | Manrope (400/500) |
| Editorial / Luxury | Playfair Display (400/italic) | Inter (400/500) |
| Modern Dynamic | Unbounded (400/500) | Manrope (400/500) |

Hammasi Google Fonts'da bor va Cyrillic'ni qo'llab-quvvatlaydi. `next/font` orqali self-host qilinadi (tez yuklanadi, GDPR uchun ham to'g'ri). Logodagi qo'lyozma shrift boshqa joyda ishlatilmaydi.

## 5. Uchta vizual yo'nalish

Har biri uchun bosh sahifa (birinchi 3–4 ekran) **desktop 1440 / tablet 834 / mobile 390** o'lchamlarida tayyorlanadi. Barchasida haqiqiy Rokate suratlari ishlatiladi.

### Direction 1 — Premium Minimal
- **G'oya:** havo ko'p, mayin fon, katta suratlar, kam matn. "Dubaydagi qimmat restoran" hissi.
- **Hero:** to'liq ekranli surat (yaxta dasturxoni, IMG_0897). Pastda chap tomonda ingichka serif sarlavha, ikkita ixcham tugma.
- **Grid:** 12 ustunli, keng chetlar (desktop 120 px). Bo'limlar orasida katta oraliq.
- **Detallar:** ingichka oltin chiziqlar, kichik harflar bilan yozilgan kichik sarlavhalar (eyebrow).
- **Harakat:** faqat mayin fade-in, rasm hover'da sekin zoom.
- **Kimga mos:** Romanning "чисто, дорого, без пафоса" talabiga eng yaqin. Eng tez va eng oson qo'llab-quvvatlanadi.

### Direction 2 — Editorial / Luxury Catering
- **G'oya:** jurnal sahifasi. Katta serif sarlavhalar, asimmetrik kompozitsiya, surat va matn "kesishadi".
- **Hero:** ekranning yarmida juda katta sarlavha (*"We cook. You celebrate."*), yonida vertikal surat (IMG_8586, oshpaz BBQ bilan).
- **Grid:** asimmetrik, rasmlar har xil o'lchamda, raqamlangan bo'limlar (01, 02, 03).
- **Detallar:** italic urg'ular, ko'proq `sand` va `green-deep` fonli bloklar, iqtibos uslubidagi bloklar.
- **Harakat:** parallax yengil, matn qatorlab chiqadi.
- **Kimga mos:** premium hospitality va event brendlari darajasi. Kontent kam bo'lsa ham boy ko'rinadi.

### Direction 3 — Modern Dynamic
- **G'oya:** zamonaviy digital. Yumaloq kartochkalar, gorizontal skroll, interaktiv elementlar.
- **Hero:** qisqa looped video (yaxtadagi tadbir), ustida sarlavha. Pastda "marquee" yo'lakchasi: *Yacht · Villa · Corporate · Birthday · BBQ...*
- **Grid:** kartochkalar, bento-grid portfolio, "We work — you relax" scroll-story ko'rinishida (qadamlar skroll bilan almashadi).
- **Detallar:** laym rang shu yerda ko'proq ishlatiladi (badge, hover), lekin fon baribir och.
- **Harakat:** scroll effektlar, magnit tugmalar. ⚠️ Roman ortiqcha animatsiya istamaydi, shuning uchun `prefers-reduced-motion` va mobil uchun yengillashtirilgan versiya bo'ladi.
- **Kimga mos:** yoshroq auditoriya va Instagram'dan keladiganlar. Video kontent ko'p bo'lsa kuchli chiqadi.

### Taqqoslash (Romanga ko'rsatish uchun)

| | Minimal | Editorial | Dynamic |
|---|---|---|---|
| Premium hissi | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Yuklanish tezligi | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Kontent kam bo'lganda ko'rinish | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Video kerakmi | Yo'q | Yo'q | Ha |
| Ishlab chiqish murakkabligi | Past | O'rta | Yuqori |

**Shaxsiy tavsiya (Romanga aytish shart emas):** Editorial yoki Minimal. Kontent asosan yaxtadan va suratlar kam, Roman tezlikni va soddalikni xohlaydi.

## 6. Komponentlar ro'yxati

Header (shaffof → skrollda oq) · Til almashtirgich · Mobil menyu (to'liq ekran) · **Mobil pastki panel** (WhatsApp / Call / Request) · Hero (rasm yoki video) · Bo'lim sarlavhasi (eyebrow + H2) · Xizmat kartochkasi · Paket kartochkasi · Taklif banneri · Afzallik elementi · Qadamlar (steps) · Ikon to'ri · Portfolio kartochkasi · Galereya + Lightbox · FAQ akkordeon · Forma maydonlari · Tugmalar (primary / secondary / whatsapp) · Footer · Toast (forma yuborildi).

## 7. Mobil (ustuvor)

- Dizayn **mobile-first** chiziladi, desktop keyin.
- Hero mobilda: vertikal surat, sarlavha ≤ 2 qator, ikkala CTA ham birinchi ekranda ko'rinadi.
- Pastki panel doim ko'rinadi, lekin forma ochilganda yashiriladi.
- Bosiladigan elementlar ≥ 44 px. Telefon raqami `tel:` havola bilan.
- Menyu va paketlar mobilda gorizontal kategoriya chip'lari bilan ko'rsatiladi, yumshoq skroll.
- Galereya swipe bilan ishlaydi.

## 8. Fotosuratlar bo'yicha qoidalar

- Hero va katta bloklar uchun faqat eng yaxshi kadrlar ishlatiladi (ro'yxat: [10](10-kontent-va-materiallar.md)).
- Yagona rang ishlovi: biroz iliq, kontrast mayin. Sayt bir xil ko'rinishi uchun barcha suratlarga qo'llaniladi.
- AI bilan yaratilgan suratlar "bizning jamoa" yoki "bizning tadbir" deb **ko'rsatilmaydi**.

## 9. Referenslar (Romanga yuboriladigan)

Yo'nalishlar bilan birga 3–5 ta haqiqiy premium catering va hospitality sayti ko'rsatiladi (Dubay va xalqaro). Aniq ro'yxat vizual konsepsiyalar tayyorlanayotganda tuziladi va havolalari tekshiriladi.
