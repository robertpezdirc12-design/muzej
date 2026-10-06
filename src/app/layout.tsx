import type { Metadata } from "next";
import { Geist, Geist_Mono, Fraunces } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";

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
    "Muzej vasi Griblje je večjezični digitalni muzej resnične vasi v Beli krajini: 113 zapisov, 589 dokazljivih virov, lestvica zanesljivosti, odprti podatki in časovnica od leta 1468.",
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
  openGraph: {
    title: "Muzej vasi Griblje — digitalni muzej vasi ob Kolpi",
    description:
      "Digitalni muzej resnične vasi v Beli krajini: 113 zapisov, 589 dokazljivih virov, lestvica zanesljivosti, odprti podatki.",
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
      "Digitalni muzej resnične vasi v Beli krajini: 113 zapisov, 589 dokazljivih virov, odprti podatki.",
    images: ["/og-card.jpg"],
  },
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
        "Večjezični digitalni muzej resnične vasi v Beli krajini (občina Črnomelj, Slovenija): 113 zapisov s trajnimi muzejskimi številkami, 589 dokazljivih virov, lestvica zanesljivosti in odprti podatki.",
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
        "Odprti podatki digitalnega muzeja: 113 zapisov o vasi Griblje z dokazljivimi viri, lestvico zanesljivosti, časovnico in zemljevidom.",
      url: `${SITE_URL}/api/opendata`,
      creator: { "@id": `${SITE_URL}/#museum` },
      license: "https://creativecommons.org/licenses/by-sa/4.0/",
      distribution: [
        { "@type": "DataDownload", encodingFormat: "application/json", contentUrl: `${SITE_URL}/api/exhibits` },
        { "@type": "DataDownload", encodingFormat: "application/json", contentUrl: `${SITE_URL}/api/events` },
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
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <Toaster />
      </body>
    </html>
  );
}
