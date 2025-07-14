import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Makers Tech - Tu Tienda de Tecnología con IA",
  description: "Experiencia de compra personalizada con asistente virtual inteligente, recomendaciones basadas en IA y gestión de inventario en tiempo real.",
  keywords: "tecnología, ecommerce, inteligencia artificial, chatbot, recomendaciones personalizadas",
  authors: [{ name: "Makers Tech" }],
  robots: "index, follow",
  openGraph: {
    title: "Makers Tech - Tu Tienda de Tecnología con IA",
    description: "Descubre la experiencia de compra del futuro con nuestro asistente virtual inteligente",
    type: "website",
    locale: "es_MX",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
