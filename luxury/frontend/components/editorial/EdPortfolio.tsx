"use client";
import { useState } from "react";
import { Lightbox } from "@/components/Gallery";
import { Img } from "@/components/Img";
import type { Img as ImgT, Project } from "@/lib/types";

/** Jurnal sahifasidek portfolio: 1 ta katta + 2 ta kichik, qolganlari 4 ustunli qatorda; sarlavhalar rasm ostida. */
export function EdPortfolio({ items, labels, loc }: {
  items: Project[]; labels: { close: string; prev: string; next: string; photo: string }; loc: Record<string, string>;
}) {
  const [open, setOpen] = useState<ImgT[] | null>(null);
  if (!items.length) return null;
  const [first, ...rest] = items;
  const side = rest.slice(0, 2);
  const tail = rest.slice(2);

  const Card = ({ p, big = false, i }: { p: Project; big?: boolean; i: number }) => {
    const images = [p.cover, ...p.images].filter(Boolean) as ImgT[];
    return (
      <button type="button" onClick={() => setOpen(images)} className="group reveal block w-full text-left" data-event="portfolio_open" data-label={p.slug}>
        <div className="overflow-hidden">
          <Img img={p.cover} sizes={big ? "(min-width:1024px) 60vw, 100vw" : "(min-width:1024px) 25vw, 50vw"}
               className={`w-full object-cover transition-transform duration-[1.4s] group-hover:scale-[1.04] ${big ? "aspect-[4/5] lg:aspect-auto lg:h-full" : "aspect-[4/5]"}`} />
        </div>
        <div className={`mt-3 flex border-b border-ink/30 pb-3 ${big ? "items-baseline justify-between gap-4" : "flex-col gap-1"}`}>
          <h3 className={`${big ? "text-[1.9rem]" : "text-[1.25rem]"} leading-tight`}>
            <span className="ed-num mr-2 text-[0.8em]">{String(i + 1).padStart(2, "0")}</span>{p.title}
          </h3>
          <span className="ed-kicker">{p.event_type || loc[p.location_type] || ""}</span>
        </div>
      </button>
    );
  };

  return (
    <>
      <div className="mt-14 grid gap-8 lg:grid-cols-12 lg:gap-10">
        <div className="lg:col-span-7 lg:row-span-2 [&>button]:flex [&>button]:h-full [&>button]:flex-col [&>button>div:first-child]:flex-1"><Card p={first} big i={0} /></div>
        {side.map((p, i) => <div key={p.slug} className="lg:col-span-5"><Card p={p} i={i + 1} /></div>)}
      </div>
      {tail.length > 0 && (
        <div className="mt-10 grid grid-cols-2 gap-6 lg:grid-cols-4 lg:gap-10">
          {tail.map((p, i) => <Card key={p.slug} p={p} i={i + 3} />)}
        </div>
      )}
      {open && <Lightbox images={open} index={0} onClose={() => setOpen(null)} labels={labels} />}
    </>
  );
}
