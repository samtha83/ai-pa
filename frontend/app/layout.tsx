import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Healthcare Provider Workspace",
  description: "Local MVP workspace shell",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
