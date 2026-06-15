import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import PageLayout from "./PageLayout";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "DocPulse Intelligence - Enterprise Document Intelligence",
  description: "Enterprise tier document intelligence platform with advanced RAG, OCR extraction, and secure classifications.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} h-full dark`}>
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-full bg-background text-on-background font-sans antialiased">
        <PageLayout>{children}</PageLayout>
      </body>
    </html>
  );
}

