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

export const metadata: Metadata = {
  title: "Muzej vasi Griblje — digitalni muzej vasi ob Kolpi",
  description:
    "Muzej vasi Griblje je večjezični digitalni muzej resnične vasi v Beli krajini: 114 zapisov, dokazljivi viri, lestvica zanesljivosti, odprti podatki in zemljevid.",
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
      "Digitalni muzej resnične vasi v Beli krajini: 114 zapisov, dokazljivi viri, lestvica zanesljivosti, odprti podatki.",
    locale: "sl_SI",
    type: "website",
  },
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
        <Toaster />
      </body>
    </html>
  );
}
