import type { Metadata } from "next";
import { EdPortfolio } from "@/components/editorial/EdPortfolio";
import { EdAbout, EdDirections, EdHead, EdHero, EdPackages, EdRelax, EdServices, EdWhy } from "@/components/editorial/Sections";
import { FaqAccordion } from "@/components/FaqAccordion";
import { JsonLd } from "@/components/JsonLd";
import { RequestSection } from "@/components/sections/RequestSection";
import { api } from "@/lib/api";
import { isLocale, t } from "@/lib/i18n";
import { buildMeta } from "@/lib/seo";
import { absolute, SITE_URL, waLink } from "@/lib/site";
import type { HomeData, Locale, SiteData } from "@/lib/types";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) return {};
  const [home, site] = await Promise.all([api<HomeData>("home", locale), api<SiteData>("site", locale)]);
  const meta = buildMeta(locale, "/", home?.seo ?? null, site, site?.seo.title);
  return { ...meta, title: { absolute: String(meta.title) } };
}

/** Bosh sahifa — Direction 2: Editorial / Luxury Catering */
export default async function HomePage({ params }: Props) {
  const { locale: l } = await params;
  const locale = l as Locale;
  const [home, site] = await Promise.all([api<HomeData>("home", locale), api<SiteData>("site", locale)]);
  if (!home || !site) return null;
  const d = t(locale);
  const wa = waLink(site.whatsapp_number, site.whatsapp_text);

  const org = {
    "@context": "https://schema.org",
    "@type": ["Organization", "LocalBusiness"],
    name: site.company_name,
    url: SITE_URL,
    description: site.seo.description || undefined,
    image: absolute(home.hero.image?.src),
    ...(site.phone ? { telephone: site.phone } : {}),
    ...(site.email ? { email: site.email } : {}),
    ...(site.instagram_url ? { sameAs: [site.instagram_url] } : {}),
    areaServed: site.service_area || "Dubai",
    address: { "@type": "PostalAddress", addressLocality: "Dubai", addressCountry: "AE" },
  };
  const faqLd = home.faq.items.length ? {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: home.faq.items.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })),
  } : null;

  return (
    <>
      <JsonLd data={faqLd ? [org, faqLd] : org} />
      <EdHero hero={home.hero} aside={home.about.image} wa={wa} waLabel={d.cta.whatsapp} cta={home.hero.cta || d.cta.proposal} area={site.service_area} />
      <EdAbout about={home.about} />
      <EdDirections data={home.directions} formats={home.formats} locale={locale} more={d.cta.learnMore} kicker={d.nav.services} />
      <EdPackages data={home.packages} offers={home.offers} locale={locale} kicker={d.nav.packages} />
      <EdRelax data={home.relax} cta={d.cta.planEvent} />
      <EdServices data={home.services} kicker={locale === "ru" ? "Под ключ" : "Turnkey"} />
      {home.portfolio.items.length > 0 && (
        <section id="portfolio" className="border-t border-ink/80 py-20 lg:py-32" data-section="portfolio">
          <div className="container-x">
            <EdHead n="06" kicker={d.nav.portfolio} title={home.portfolio.title} text={home.portfolio.text} />
            <EdPortfolio items={home.portfolio.items} labels={{ close: d.close, prev: d.prev, next: d.next, photo: d.photo }} loc={d.loc} />
          </div>
        </section>
      )}
      <EdWhy data={home.why} />
      {home.faq.items.length > 0 && (
        <section className="border-t border-ink/80 py-20 lg:py-28" data-section="faq">
          <div className="container-x grid gap-10 lg:grid-cols-12">
            <div className="lg:col-span-4"><EdHead n="08" kicker="FAQ" title={home.faq.title} /></div>
            <div className="lg:col-span-8"><FaqAccordion items={home.faq.items} /></div>
          </div>
        </section>
      )}
      <RequestSection locale={locale} site={site} title={home.form.title} text={home.form.text} packages={home.packages.items} source="/" />
    </>
  );
}
