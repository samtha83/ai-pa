"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import {
  ClientForm,
  type ClientFormValues,
} from "@/components/client-form";
import { WorkspaceShell } from "@/components/workspace-shell";
import {
  fetchClient,
  updateClient,
  type ClientRecord,
  type ClientWrite,
} from "@/lib/api";

function toFormValues(client: ClientRecord): ClientFormValues {
  return {
    name: client.name,
    email: client.email ?? "",
    phone: client.phone ?? "",
    timezone: client.timezone,
    service_type: client.service_type ?? "",
    goals: client.goals.join("\n"),
    status: client.status,
  };
}

export default function ClientDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [client, setClient] = useState<ClientRecord | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    let isCurrent = true;
    setIsLoading(true);
    setLoadError(null);
    fetchClient(id)
      .then((record) => {
        if (isCurrent) {
          setClient(record);
        }
      })
      .catch((error: unknown) => {
        if (isCurrent) {
          setLoadError(
            error instanceof Error ? error.message : "Unable to load client.",
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
  }, [id]);

  async function handleUpdate(values: ClientWrite): Promise<boolean> {
    setIsSaving(true);
    setSaveError(null);
    setNotice(null);
    try {
      const saved = await updateClient(id, values);
      setClient(saved);
      setNotice("Client details saved.");
      return true;
    } catch (error) {
      setSaveError(
        error instanceof Error ? error.message : "Unable to save client.",
      );
      return false;
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <WorkspaceShell
      title={client?.name ?? "Client details"}
      description="Review and update the saved client profile."
    >
      <p className="mb-5 text-sm">
        <Link className="font-medium text-blue-700 hover:underline" href="/clients">
          Back to clients
        </Link>
      </p>

      {isLoading ? (
        <p className="rounded-lg border border-slate-200 bg-white p-5 text-sm text-slate-600" role="status">
          Loading client details...
        </p>
      ) : loadError ? (
        <p className="rounded-lg border border-red-200 bg-red-50 p-5 text-sm text-red-700" role="alert">
          Unable to load client: {loadError}
        </p>
      ) : client ? (
        <section className="max-w-2xl rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-5 flex items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold text-slate-900">
                Client profile
              </h2>
              <p className="mt-1 text-sm text-slate-600">
                Last updated {client.updated_at.slice(0, 10)}
              </p>
            </div>
            <span
              className={`rounded-full px-2.5 py-1 text-xs font-semibold capitalize ${
                client.status === "active"
                  ? "bg-emerald-100 text-emerald-800"
                  : "bg-slate-100 text-slate-700"
              }`}
            >
              {client.status}
            </span>
          </div>
          {saveError ? (
            <p className="mb-4 text-sm text-red-700" role="alert">
              Unable to save client: {saveError}
            </p>
          ) : null}
          {notice ? (
            <p className="mb-4 text-sm text-emerald-700" role="status">
              {notice}
            </p>
          ) : null}
          <ClientForm
            initialValues={toFormValues(client)}
            isSubmitting={isSaving}
            key={`${client.id}-${client.updated_at}`}
            onSubmit={handleUpdate}
            submitLabel="Save client"
          />
        </section>
      ) : null}
    </WorkspaceShell>
  );
}
