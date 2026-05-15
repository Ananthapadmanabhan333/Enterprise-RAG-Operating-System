import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AetherOS | Enterprise RAG Intelligence",
  description: "Autonomous Enterprise RAG Operating System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-background text-foreground min-h-screen">
        {children}
      </body>
    </html>
  );
}
