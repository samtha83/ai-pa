"use client";

import { useEffect, useState, type FormEvent } from "react";

import { WorkspaceShell } from "@/components/workspace-shell";
import { getStoredSession, setStoredSession } from "@/lib/auth";
import {
  fetchProviderProfile,
  updateProviderProfile,
  type ProviderProfile,
} from "@/lib/api";

type ProfileFields = {
  name: string;
  business_name: string;
  timezone: string;
};

function toFields(profile: ProviderProfile): ProfileFields {
  return {
    name: profile.name,
    business_name: profile.business_name ?? "",
    timezone: profile.timezone,
  };
}

export default function SettingsPage() {
  const [fields, setFields] = useState<ProfileFields>({
    name: "",
    business_name: "",
    timezone: "UTC",
  });
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    let isCurrent = true;
    fetchProviderProfile()
      .then((profile) => {
        if (isCurrent) {
          setFields(toFields(profile));
          setLoadError(null);
        }
      })
      .catch((error: unknown) => {
        if (isCurrent) {
          setLoadError(
            error instanceof Error
              ? error.message
              : "Unable to load provider settings.",
          );
        }
      })
      .finally(() => {
        if (isCurrent) {
          setIsLoading(false);
        }
      });

    return () => {
      isCurrent = false;
    };
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSaving(true);
    setSaveError(null);
    setNotice(null);

    try {
      const profile = await updateProviderProfile({
        name: fields.name.trim(),
        business_name: fields.business_name.trim() || null,
        timezone: fields.timezone.trim(),
      });
      setFields(toFields(profile));
      const session = getStoredSession();
      if (session) {
        setStoredSession({
          ...session,
          providerName: profile.name,
          businessName: profile.business_name ?? undefined,
        });
      }
      setNotice("Provider profile saved.");
    } catch (error) {
      setSaveError(
        error instanceof Error
          ? error.message
          : "Unable to save provider settings.",
      );
    } finally {
      setIsSaving(false);
    }
  }

  const inputClassName =
    "mt-1 block w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200";

  return (
    <WorkspaceShell
      title="Provider Settings"
      description="Review and update the profile used by your provider workspace."
    >
      <div className="max-w-2xl rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        {isLoading ? (
          <p role="status" className="text-sm text-slate-600">
            Loading provider settings...
          </p>
        ) : loadError ? (
          <p role="alert" className="text-sm text-red-700">
            Unable to load provider settings: {loadError}
          </p>
        ) : (
          <form className="space-y-5" onSubmit={handleSubmit}>
            <label className="block text-sm font-medium text-slate-700">
              Provider name
              <input
                autoComplete="name"
                className={inputClassName}
                maxLength={255}
                onChange={(event) =>
                  setFields((current) => ({
                    ...current,
                    name: event.target.value,
                  }))
                }
                required
                value={fields.name}
              />
            </label>

            <label className="block text-sm font-medium text-slate-700">
              Business name
              <input
                autoComplete="organization"
                className={inputClassName}
                maxLength={255}
                onChange={(event) =>
                  setFields((current) => ({
                    ...current,
                    business_name: event.target.value,
                  }))
                }
                value={fields.business_name}
              />
            </label>

            <label className="block text-sm font-medium text-slate-700">
              Timezone
              <input
                className={inputClassName}
                maxLength={64}
                onChange={(event) =>
                  setFields((current) => ({
                    ...current,
                    timezone: event.target.value,
                  }))
                }
                required
                value={fields.timezone}
              />
            </label>

            {saveError ? (
              <p role="alert" className="text-sm text-red-700">
                Unable to save provider settings: {saveError}
              </p>
            ) : null}
            {notice ? (
              <p role="status" className="text-sm text-emerald-700">
                {notice}
              </p>
            ) : null}
            <button
              className="inline-flex items-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
              disabled={isSaving}
              type="submit"
            >
              {isSaving ? "Saving..." : "Save profile"}
            </button>
          </form>
        )}
      </div>
    </WorkspaceShell>
  );
}
