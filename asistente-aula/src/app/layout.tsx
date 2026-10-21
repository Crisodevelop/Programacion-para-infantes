import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Asistente de aula",
  description: "Mando por voz para la clase",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  // El mando es un botón que se mantiene pulsado: el zoom por doble toque
  // sería un accidente constante en el bolsillo.
  userScalable: false,
  themeColor: "#070d18",
};

export default function Raiz({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
