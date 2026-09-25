"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { WorkspaceShell } from "@/components/workspace-shell";
import { loginToDemoProvider } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleLogin() {
    setIsSubmitting(true);
    setError(null);

    try {
      await loginToDemoProvider();
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to sign in.");
      setIsSubmitting(false);
    }
  }

  return (
    <WorkspaceShell
      title="Demo Provider Login"
      description="Local development authentication for the provider workspace. This flow is intentionally limited to the MVP and should be replaced before production use."
    >
      <div className="rounded-xl border border-amber-200 bg-amber-50 p-6">
        <div className="space-y-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-amber-700">Demo auth</p>
            <h2 className="mt-2 text-xl font-semibold text-slate-900">Sign in as the local demo provider</h2>
          </div>

          <p className="text-sm text-slate-700">
            This login is for local development only and uses a server-validated session cookie. Provider identity is resolved on the backend and never trusted from the browser.
          </p>

          <button
            type="button"
            onClick={handleLogin}
            disabled={isSubmitting}
            className="inline-flex items-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
          >
            {isSubmitting ? "Signing in..." : "Log in as Demo Provider"}
          </button>

          {error ? <p className="text-sm text-red-700">{error}</p> : null}
        </div>
      </div>
    </WorkspaceShell>
  );
}
