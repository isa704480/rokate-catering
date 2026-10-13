import type { NextConfig } from "next";

const API = process.env.API_INTERNAL_URL || "http://localhost:8002";

// DEMO: backend yo'q — ma'lumot frontend ichidagi lib/demo-data.json dan
const DEMO = process.env.DEMO_MODE === "1" || (!!process.env.VERCEL && !process.env.API_INTERNAL_URL);

const nextConfig: NextConfig = {
  env: { NEXT_PUBLIC_DEMO_MODE: DEMO ? "1" : "0" },
  output: "standalone",
  poweredByHeader: false,
  // Production'da /api/v1 va /media'ni Caddy to'g'ridan-to'g'ri Django'ga yuboradi.
  // Bu rewrite'lar lokal ishlab chiqish uchun (va zaxira sifatida).
  async rewrites() {
    if (DEMO) return [];
    return [
      { source: "/api/v1/:path*", destination: `${API}/api/v1/:path*` },
      { source: "/api/panel/:path*", destination: `${API}/api/panel/:path*` },
      { source: "/media/:path*", destination: `${API}/media/:path*` },
    ];
  },
};

export default nextConfig;
