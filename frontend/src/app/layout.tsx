import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Content Factory",
  description: "Multi-agent content orchestration with HITL",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>{children}</Providers>
        <footer className="text-center text-xs text-muted py-4">
          <a href="/terms" className="hover:underline">
            Terms
          </a>
          {" · "}
          <a href="/privacy" className="hover:underline">
            Privacy
          </a>
        </footer>
      </body>
    </html>
  );
}
