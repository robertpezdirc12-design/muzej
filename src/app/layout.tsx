import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono, Fraunces } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";
import { ServiceWorkerRegistrar } from "@/components/museum/sw-registrar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin", "latin-ext"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin", "latin-ext"],
});

const fraunces = Fraunces({
  variable: "--font-fraunces",
  subsets: ["latin", "latin-ext"],
  display: "swap",
});

const SITE_URL = "https://griblje-museum.vercel.app";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: "Muzej vasi Griblje — digitalni muzej vasi ob Kolpi",
  description:
    "Muzej vasi Griblje je večjezični digitalni muzej resnične vasi v Beli krajini: 114 zapisov, 596 dokazljivih virov, ATLAS 1825 (franciscejski kataster, georeferencirana lista, register hiš), raziskave in provenienca, AR vodnik, odprti podatki in časovnica od leta 1468.",
  keywords: [
    "Griblje",
    "Muzej",
    "Bela krajina",
    "Kolpa",
    "Črnomelj",
    "digitalni muzej",
    "vas",
    "zgodovina",
    "etnografija",
  ],
  manifest: "/manifest.webmanifest",
  icons: {
    icon: [
      { url: "/icon.svg", type: "image/svg+xml" },
      { url: "/icons/icon-192.png", sizes: "192x192", type: "image/png" },
      { url: "/icons/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: [{ url: "/icons/apple-touch-icon.png", sizes: "180x180" }],
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "Muzej Griblje",
  },
  openGraph: {
    title: "Muzej vasi Griblje — digitalni muzej vasi ob Kolpi",
    description:
      "Digitalni muzej resnične vasi v Beli krajini: 114 zapisov, 596 dokazljivih virov, lestvica zanesljivosti, odprti podatki.",
    url: SITE_URL,
    siteName: "Muzej vasi Griblje",
    locale: "sl_SI",
    type: "website",
    images: [
      {
        url: "/og-card.jpg",
        width: 1200,
        height: 630,
        alt: "Muzej vasi Griblje — digitalni muzej vasi ob Kolpi",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Muzej vasi Griblje — digitalni muzej vasi ob Kolpi",
    description:
      "Digitalni muzej resnične vasi v Beli krajini: 114 zapisov, 596 dokazljivih virov, odprti podatki.",
    images: ["/og-card.jpg"],
  },
};

/* Tema PWA: spojitev z glavo strani (smetana / temna zelena) */
export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#F7F3EB" },
    { media: "(prefers-color-scheme: dark)", color: "#0F1610" },
  ],
  width: "device-width",
  initialScale: 1,
};

/* JSON-LD: muzej in odprti podatki zbirke */
const jsonLd = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Museum",
      "@id": `${SITE_URL}/#museum`,
      name: "Muzej vasi Griblje",
      alternateName: "Griblje Village Museum",
      url: SITE_URL,
      description:
        "Večjezični digitalni muzej resnične vasi v Beli krajini (občina Črnomelj, Slovenija): 114 zapisov s trajnimi muzejskimi številkami, 596 dokazljivih virov, lestvica zanesljivosti in odprti podatki.",
      foundingDate: "2026",
      inLanguage: ["sl", "en"],
      logo: `${SITE_URL}/logo.svg`,
      image: `${SITE_URL}/og-card.jpg`,
      isAccessibleForFree: true,
    },
    {
      "@type": "Dataset",
      name: "Zbirka Muzeja vasi Griblje (MVG-001–114)",
      description:
        "Odprti podatki digitalnega muzeja: 114 zapisov o vasi Griblje z dokazljivimi viri, lestvico zanesljivosti, časovnico, zemljevidom, Atlasom 1825 in provenienčnim poročilom.",
      url: `${SITE_URL}/api/opendata`,
      creator: { "@id": `${SITE_URL}/#museum` },
      license: "https://creativecommons.org/licenses/by-sa/4.0/",
      distribution: [
        { "@type": "DataDownload", encodingFormat: "application/json", contentUrl: `${SITE_URL}/api/exhibits` },
        { "@type": "DataDownload", encodingFormat: "application/json", contentUrl: `${SITE_URL}/api/events` },
        { "@type": "DataDownload", encodingFormat: "application/json", contentUrl: `${SITE_URL}/api/atlas` },
        { "@type": "DataDownload", encodingFormat: "application/json", contentUrl: `${SITE_URL}/api/provenance` },
        { "@type": "DataDownload", encodingFormat: "application/json", contentUrl: `${SITE_URL}/api/coverage` },
        { "@type": "DataDownload", encodingFormat: "application/json", contentUrl: `${SITE_URL}/api/qa` },
      ],
      inLanguage: ["sl", "en"],
      isAccessibleForFree: true,
    },
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="sl" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${fraunces.variable} antialiased bg-background text-foreground`}
      >
        {children}
        <ServiceWorkerRegistrar />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <Toaster />
      </body>
    </html>
  );
}
