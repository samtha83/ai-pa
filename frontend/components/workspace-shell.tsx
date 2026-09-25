"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import { clearStoredSession, getStoredSession, logoutFromDemoProvider } from "@/lib/auth";

const routes = [
  { href: "/login", label: "Login" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/clients", label: "Clients" },
  { href: "/calendar", label: "Calendar" },
  { href: "/settings", label: "Settings" },
];

export function WorkspaceShell({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children?: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const session = getStoredSession();

  async function handleLogout() {
    try {
      await logoutFromDemoProvider();
    } finally {
      clearStoredSession();
      router.push("/login");
    }
  }

  return (
    <main className="min-h-screen bg-slate-100 p-4 text-slate-900 sm:p-8">
      <div className="mx-auto max-w-6xl overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <header className="border-b border-slate-200 bg-slate-50 px-6 py-5 sm:px-8">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-blue-600">
                Provider workspace
              </p>
              <h1 className="mt-3 text-2xl font-bold text-slate-900 sm:text-3xl">{title}</h1>
              <p className="mt-2 max-w-2xl text-sm text-slate-600 sm:text-base">{description}</p>
            </div>

            {session ? (
              <div className="flex items-center gap-3 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700">
                <span className="rounded-full bg-emerald-100 px-2 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-emerald-700">
                  Demo provider
                </span>
                <span className="font-medium">{session.providerName}</span>
                <button
                  type="button"
                  onClick={handleLogout}
                  className="rounded-md border border-slate-300 px-2 py-1 text-xs font-medium text-slate-700 transition hover:border-red-400 hover:text-red-700"
                >
                  Log out
                </button>
              </div>
            ) : (
              <div className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800">
                Local-only auth
              </div>
            )}
          </div>
        </header>

        <nav aria-label="Main navigation" className="border-b border-slate-200 bg-white px-6 py-4 sm:px-8">
          <ul className="flex flex-wrap gap-2">
            {routes.map((route) => {
              const isActive = pathname === route.href;
              return (
                <li key={route.href}>
                  <Link
                    href={route.href}
                    aria-current={isActive ? "page" : undefined}
                    className="inline-flex items-center rounded-md border border-slate-300 bg-slate-50 px-3 py-2 text-sm font-medium text-slate-700 transition duration-150 hover:border-blue-500 hover:bg-blue-50 hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  >
                    {route.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        <section className="px-6 py-6 sm:px-8 sm:py-8">{children}</section>
      </div>
    </main>
  );
}
