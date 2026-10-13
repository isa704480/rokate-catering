import type { Metadata } from "next";
import { JsonLd } from "@/components/JsonLd";
import { SectionHead } from "@/components/SectionHead";
import { About } from "@/components/sections/About";
import { Directions } from "@/components/sections/Directions";
import { ExtraServices } from "@/components/sections/ExtraServices";
import { Hero } from "@/components/sections/Hero";
import { Packages } from "@/components/sections/Packages";
import { Portfolio } from "@/components/sections/Portfolio";
import { Relax } from "@/components/sections/Relax";
import { RequestSection } from "@/components/sections/RequestSection";
import { FaqSection, WhyUs } from "@/components/sections/WhyFaq";
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

export default async function HomePage({ params }: Props) {
  const { locale: l } = await params;
  const locale = l as Locale;
  const [home, site] = await Promise.all([api<HomeData>("home", locale), api<SiteData>("site", locale)]);
  if (!home || !site) return null;
  const d = t(locale);
  const wa = waLink(site.whatsapp_number, site.whatsapp_text);
  const req = "#request";

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
      <Hero hero={{ ...home.hero, cta: home.hero.cta || d.cta.proposal }} wa={wa} waLabel={d.cta.whatsapp} ctaHref={req} area={site.service_area} />
      <About about={home.about} />
      <Directions data={home.directions} formats={home.formats} locale={locale} more={d.cta.learnMore} requestHref={req} eyebrow={d.nav.services} />
      <Packages data={home.packages} offers={home.offers} locale={locale} eyebrow={d.nav.packages} />
      <Relax data={home.relax} cta={d.cta.planEvent} ctaHref={req} />
      <ExtraServices data={home.services} eyebrow={locale === "ru" ? "Под ключ" : "Turnkey"} />
      {home.portfolio.items.length > 0 && (
        <section id="portfolio" className="section pt-0 lg:pt-0" data-section="portfolio">
          <div className="container-x">
            <SectionHead eyebrow={d.nav.portfolio} title={home.portfolio.title} text={home.portfolio.text} className="md:-mb-20" />
            <Portfolio items={home.portfolio.items} labels={{ close: d.close, prev: d.prev, next: d.next, photo: d.photo }} loc={d.loc} />
          </div>
        </section>
      )}
      <WhyUs data={home.why} />
      <FaqSection title={home.faq.title} items={home.faq.items} eyebrow="FAQ" />
      <RequestSection locale={locale} site={site} title={home.form.title} text={home.form.text}
                      packages={home.packages.items} source="/" />
    </>
  );
}
