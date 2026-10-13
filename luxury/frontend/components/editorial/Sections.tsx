/**
 * Direction 2 — Editorial / Luxury Catering.
 * Jurnal sahifasidek: raqamlangan bo'limlar (01, 02...), katta Playfair sarlavhalar,
 * ingichka qora chiziqlar, menyu-karta ko'rinishidagi paketlar.
 */
import Link from "next/link";
import { WhatsAppIcon } from "@/components/Icon";
import { Img } from "@/components/Img";
import { RequestPackageButton } from "@/components/RequestPackageButton";
import { formatPrice, t } from "@/lib/i18n";
import { href, paragraphs } from "@/lib/site";
import type { HomeData, Locale } from "@/lib/types";

const roman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"];

/** Bo'lim sarlavhasi: "02 — Where we cater" */
export function EdHead({ n, kicker, title, text, light = false, center = false, small = false }: {
  n: string; kicker: string; title?: string; text?: string; light?: boolean; center?: boolean; small?: boolean;
}) {
  return (
    <div className={`reveal ${center ? "mx-auto max-w-3xl text-center" : ""}`}>
      <p className={`ed-kicker flex items-center gap-3 ${center ? "justify-center" : ""} ${light ? "!text-white/70" : ""}`}>
        <span className="ed-num text-[15px] tracking-normal normal-case">{n}</span>
        <span className={`h-px w-10 ${light ? "bg-white/50" : "bg-ink/60"}`} />
        {kicker}
      </p>
      {title && <h2 className={`mt-5 leading-[1.02] ${small ? "text-[clamp(2.2rem,3.4vw,3.2rem)]" : "text-[clamp(2.4rem,5vw,4.4rem)]"} ${light ? "text-white" : ""}`}>{title}</h2>}
      {text && <p className={`mt-5 max-w-xl text-[17px] leading-relaxed ${center ? "mx-auto" : ""} ${light ? "text-white/75" : "text-ink-muted"}`}>{text}</p>}
    </div>
  );
}

/* ------------------------------------------------------------------ HERO */
export function EdHero({ hero, aside, wa, waLabel, cta, area }: {
  hero: HomeData["hero"]; aside: HomeData["about"]["image"]; wa: string; waLabel: string; cta: string; area?: string;
}) {
  return (
    <section className="relative overflow-hidden" data-section="hero">
      <div className="container-x pt-10 lg:pt-16">
        <div className="flex items-center justify-between border-b border-ink/80 pb-3 ed-kicker">
          <span>{hero.eyebrow}</span>
          <span className="hidden sm:inline">{area}</span>
        </div>
        <h1 className="reveal mt-8 text-[clamp(3rem,9.2vw,9.4rem)] leading-[0.9] tracking-[-0.02em] lg:mt-12">
          {hero.title}
        </h1>
      </div>

      <div className="container-x mt-10 grid gap-8 pb-16 lg:mt-16 lg:grid-cols-12 lg:gap-10 lg:pb-28">
        <figure className="reveal lg:col-span-5">
          <div className="relative aspect-[4/5] overflow-hidden">
            <Img img={hero.image} priority sizes="(min-width:1024px) 40vw, 100vw" className="h-full w-full object-cover" />
          </div>
          <figcaption className="mt-3 flex justify-between ed-kicker"><span>Rokate Catering</span><span className="ed-num text-[14px] normal-case tracking-normal">fig. 1</span></figcaption>
        </figure>

        <div className="reveal flex flex-col justify-between gap-10 lg:col-span-3 lg:py-6">
          <p className="text-[19px] leading-relaxed text-ink">{hero.subtitle}</p>
          <div className="flex flex-col gap-3">
            <a href="#request" className="btn btn-primary w-full" data-event="cta_click" data-location="hero">{cta}</a>
            {wa && (
              <a href={wa} target="_blank" rel="noopener" className="btn btn-outline w-full" data-location="hero">
                <WhatsAppIcon size={16} />{waLabel}
              </a>
            )}
          </div>
        </div>

        <figure className="reveal hidden lg:col-span-4 lg:block lg:pt-24">
          <div className="relative aspect-[3/4] overflow-hidden">
            <Img img={aside} sizes="30vw" className="h-full w-full object-cover" />
          </div>
          <figcaption className="mt-3 ed-kicker">Dubai · UAE</figcaption>
        </figure>
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ ABOUT */
export function EdAbout({ about }: { about: HomeData["about"] }) {
  if (!about.title) return null;
  const ps = paragraphs(about.text);
  return (
    <section id="about" className="border-t border-ink/80 py-20 lg:py-32" data-section="about">
      <div className="container-x">
        <EdHead n="01" kicker={about.eyebrow || "About"} />
        <blockquote className="reveal mx-auto mt-10 max-w-5xl text-center font-display text-[clamp(2rem,4.4vw,3.8rem)] italic leading-[1.12]">
          “{about.title}”
        </blockquote>
        <div className="mx-auto mt-14 grid max-w-4xl gap-8 text-[17px] leading-[1.8] text-ink-muted md:grid-cols-2 md:gap-14">
          {ps.map((p, i) => <p key={i} className={`reveal ${i === 0 ? "ed-dropcap text-ink" : ""}`}>{p}</p>)}
        </div>
        {about.stats.length > 0 && (
          <dl className="reveal mx-auto mt-16 grid max-w-4xl grid-cols-2 border-y border-ink/80 sm:grid-cols-4">
            {about.stats.map((s) => (
              <div key={s.label} className="border-ink/20 px-4 py-6 text-center [&:not(:last-child)]:border-r">
                <dd className="font-display text-[2.8rem] leading-none">{s.value}</dd>
                <dt className="mt-2 ed-kicker">{s.label}</dt>
              </div>
            ))}
          </dl>
        )}
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ DIRECTIONS (indeks ro'yxati) */
export function EdDirections({ data, formats, locale, more, kicker }: {
  data: HomeData["directions"]; formats: HomeData["formats"]; locale: Locale; more: string; kicker: string;
}) {
  if (!data.items.length) return null;
  return (
    <section id="directions" className="bg-surface py-20 lg:py-32" data-section="directions">
      <div className="container-x">
        <EdHead n="02" kicker={kicker} title={data.title} />
        <ol className="mt-14 border-t border-ink/80">
          {data.items.map((s, i) => {
            const target = s.has_page ? href(locale, `/catering/${s.slug}`) : "#request";
            const inner = (
              <div className="grid grid-cols-[auto_1fr] items-center gap-x-5 gap-y-3 py-7 md:grid-cols-[80px_1fr_1.1fr_160px] md:gap-x-8 lg:py-9">
                <span className="ed-num text-[1.6rem] md:text-[2rem]">{String(i + 1).padStart(2, "0")}</span>
                <h3 className="text-[clamp(1.9rem,3.6vw,3.2rem)] leading-none transition-transform duration-500 group-hover:translate-x-2">{s.title}</h3>
                <p className="col-span-2 text-[15px] leading-relaxed text-ink-muted md:col-span-1">
                  {s.card_text}
                  <span className="mt-3 block ed-kicker !text-ink">{more} →</span>
                </p>
                <div className="hidden overflow-hidden md:block">
                  <Img img={s.image} sizes="160px" className="aspect-[4/5] w-full object-cover grayscale-[35%] transition duration-700 group-hover:grayscale-0 group-hover:scale-105" />
                </div>
              </div>
            );
            return (
              <li key={s.slug} className="reveal group border-b border-ink/30">
                {s.has_page ? <Link href={target}>{inner}</Link> : <a href={target}>{inner}</a>}
              </li>
            );
          })}
        </ol>
        {formats.items.length > 0 && (
          <div className="reveal mt-16 text-center">
            <p className="ed-kicker">{formats.title}</p>
            <p className="mx-auto mt-5 max-w-5xl font-display text-[clamp(1.4rem,2.6vw,2.2rem)] italic leading-snug text-ink-muted">
              {formats.items.map((f, i) => (
                <span key={f}>{f}{i < formats.items.length - 1 && <> <span className="mx-2 not-italic text-gold">·</span> </>}</span>
              ))}
            </p>
          </div>
        )}
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ PACKAGES (menyu kartasi) */
export function EdPackages({ data, offers, locale, kicker }: {
  data: HomeData["packages"]; offers: HomeData["offers"]; locale: Locale; kicker: string;
}) {
  if (!data.items.length && !offers.length) return null;
  const d = t(locale);
  return (
    <section id="packages" className="py-20 lg:py-32" data-section="packages">
      <div className="container-x">
        <div className="grid gap-8 lg:grid-cols-12">
          <div className="lg:col-span-4">
            <div className="lg:sticky lg:top-28"><EdHead n="03" kicker={kicker} title={data.title} text={data.text} small /></div>
          </div>
          <div className="lg:col-span-8">
            {offers.map((o) => (
              <div key={o.id} className="reveal mb-10 grid gap-6 border border-ink/80 p-6 sm:grid-cols-[180px_1fr] sm:p-8">
                {o.image && <Img img={o.image} sizes="180px" className="aspect-square w-full object-cover" />}
                <div>
                  <p className="ed-kicker !text-gold">{d.badge.seasonal}{o.ends_at ? ` · ${d.offerUntil} ${new Date(o.ends_at).toLocaleDateString(locale === "ru" ? "ru-RU" : "en-GB", { day: "numeric", month: "long" })}` : ""}</p>
                  <h3 className="mt-3 text-[2rem] leading-tight">{o.title}</h3>
                  {o.text && <p className="mt-3 text-ink-muted">{o.text}</p>}
                  <RequestPackageButton slug={o.package || ""} label={o.cta_text || d.cta.request} className="mt-5 inline-block ed-kicker !text-ink link-underline" />
                </div>
              </div>
            ))}

            {/* Restoran menyusi kabi: ramka ichida, nom ........ narx */}
            <div className="reveal border-[3px] border-double border-ink/80 bg-surface p-6 sm:p-10">
              <p className="text-center font-display text-[1.6rem] italic">Rokate · {d.nav.packages}</p>
              <div className="mx-auto mt-2 h-px w-16 bg-gold" />
              <ul className="mt-8 space-y-10">
                {data.items.map((p, i) => {
                  const guests = d.guests(p.guests_min, p.guests_max);
                  return (
                    <li key={p.slug} className="grid gap-5 sm:grid-cols-[110px_1fr]">
                      <Img img={p.image} sizes="110px" className="aspect-square w-full max-w-[110px] object-cover" />
                      <div>
                        <div className="flex items-baseline">
                          <h3 className="text-[1.6rem] leading-tight sm:text-[1.9rem]">
                            <span className="ed-num mr-2 text-[1.1rem]">{roman[i] || i + 1}.</span>{p.name}
                          </h3>
                          <span className="ed-leader" />
                          <span className="whitespace-nowrap font-display text-[1.25rem]">
                            {p.price_from != null ? `${d.price.from} ${formatPrice(locale, p.price_from)} ${d.price.currency}` : <span className="text-[14px] italic text-ink-muted">{d.price.onRequest}</span>}
                          </span>
                        </div>
                        <p className="mt-1 ed-kicker !text-gold">{[guests, p.badge && (d.badge[p.badge] || p.badge)].filter(Boolean).join(" · ")}</p>
                        {p.short_text && <p className="mt-3 italic text-ink-muted">{p.short_text}</p>}
                        {p.contents.length > 0 && <p className="mt-2 text-[14px] leading-relaxed">{p.contents.join(" · ")}</p>}
                        <RequestPackageButton slug={p.slug} label={`${d.cta.requestPackage} →`} className="mt-4 inline-block ed-kicker !text-ink link-underline" />
                      </div>
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ WE WORK — YOU RELAX */
export function EdRelax({ data, cta }: { data: HomeData["relax"]; cta: string }) {
  if (!data.title) return null;
  return (
    <section data-section="relax">
      <div className="relative flex min-h-[78vh] items-center justify-center overflow-hidden bg-green-deep">
        <Img img={data.image} sizes="100vw" className="absolute inset-0 h-full w-full object-cover opacity-55" />
        <div className="absolute inset-0 bg-gradient-to-b from-[#0e1d19]/60 via-[#0e1d19]/30 to-[#0e1d19]/80" />
        <div className="container-x relative py-24 text-center text-white">
          <EdHead n="04" kicker={data.eyebrow || ""} light center />
          <h2 className="reveal mt-6 text-[clamp(3rem,8vw,7.5rem)] italic leading-[0.95] text-white">{data.title}</h2>
          {data.text && <p className="reveal mx-auto mt-8 max-w-2xl text-[18px] leading-relaxed text-white/80">{data.text}</p>}
        </div>
      </div>
      {data.steps.length > 0 && (
        <div className="container-x py-16 lg:py-24">
          <ol className="grid border-t border-ink/80 sm:grid-cols-2 lg:grid-cols-4">
            {data.steps.map((s, i) => (
              <li key={s.title} className="reveal border-b border-ink/20 py-8 sm:px-6 lg:border-b-0 lg:[&:not(:last-child)]:border-r first:pl-0">
                <span className="font-display text-[3rem] italic leading-none text-gold">{roman[i]}</span>
                <h3 className="mt-4 text-[1.6rem] leading-tight">{s.title}</h3>
                {s.text && <p className="mt-3 text-[15px] leading-relaxed text-ink-muted">{s.text}</p>}
              </li>
            ))}
          </ol>
          <div className="reveal mt-12 text-center"><a href="#request" className="btn btn-primary" data-event="cta_click" data-location="relax">{cta}</a></div>
        </div>
      )}
    </section>
  );
}

/* ------------------------------------------------------------------ ADDITIONAL SERVICES */
export function EdServices({ data, kicker }: { data: HomeData["services"]; kicker: string }) {
  if (!data.items.length) return null;
  return (
    <section className="bg-surface py-20 lg:py-32" data-section="services">
      <div className="container-x grid gap-12 lg:grid-cols-12">
        <div className="lg:col-span-5">
          <EdHead n="05" kicker={kicker} title={data.title} text={data.text} />
          {data.note && <p className="reveal mt-8 border-l border-gold pl-5 font-display text-[1.15rem] italic text-ink-muted">{data.note}</p>}
        </div>
        <ul className="reveal columns-1 gap-12 sm:columns-2 lg:col-span-6 lg:col-start-7">
          {data.items.map((s, i) => (
            <li key={s.title} className="flex break-inside-avoid items-baseline gap-4 border-b border-ink/20 py-4">
              <span className="ed-num w-7 text-[15px]">{String(i + 1).padStart(2, "0")}</span>
              <span className="text-[1.25rem] font-display">{s.title}</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ WHY */
export function EdWhy({ data }: { data: HomeData["why"] }) {
  if (!data.items.length) return null;
  return (
    <section className="py-20 lg:py-28" data-section="why">
      <div className="container-x">
        <EdHead n="07" kicker="Rokate" title={data.title} center />
        <div className="mt-14 grid border-y border-ink/80 sm:grid-cols-2 lg:grid-cols-4">
          {data.items.map((w, i) => (
            <div key={w.title} className="reveal border-ink/20 p-7 [&:not(:last-child)]:border-b sm:[&:nth-child(odd)]:border-r lg:border-b-0 lg:[&:not(:last-child)]:border-r">
              <span className="font-display text-[4rem] italic leading-none text-gold/80">{i + 1}</span>
              <h3 className="mt-4 text-[1.5rem] leading-tight">{w.title}</h3>
              {w.text && <p className="mt-3 text-[15px] leading-relaxed text-ink-muted">{w.text}</p>}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
