"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

import { ClientForm } from "@/components/client-form";
import { WorkspaceShell } from "@/components/workspace-shell";
import {
  createClient,
  fetchClients,
  type ClientRecord,
  type ClientWrite,
} from "@/lib/api";

export default function ClientsPage() {
  const [clients, setClients] = useState<ClientRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [listError, setListError] = useState<string | null>(null);
  const [createError, setCreateError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const loadClients = useCallback(async () => {
    setIsLoading(true);
    setListError(null);
    try {
      setClients(await fetchClients());
    } catch (error) {
      setListError(
        error instanceof Error ? error.message : "Unable to load clients.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadClients();
  }, [loadClients]);

  async function handleCreate(values: ClientWrite): Promise<boolean> {
    setIsCreating(true);
    setCreateError(null);
    setNotice(null);
    try {
      const client = await createClient(values);
      setClients((current) => [client, ...current]);
      setNotice(`${client.name} was added to your client list.`);
      return true;
    } catch (error) {
      setCreateError(
        error instanceof Error ? error.message : "Unable to create client.",
      );
      return false;
    } finally {
      setIsCreating(false);
    }
  }

  return (
    <WorkspaceShell
      title="Clients"
      description="Create and review the clients linked to your provider workspace."
    >
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1.2fr)_minmax(18rem,0.8fr)]">
        <section
          aria-labelledby="client-list-heading"
          className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
        >
          <div className="flex items-baseline justify-between gap-3">
            <h2
              className="text-lg font-semibold text-slate-900"
              id="client-list-heading"
            >
              Client list
            </h2>
            {!isLoading && !listError ? (
              <span className="text-sm text-slate-500">
                {clients.length} {clients.length === 1 ? "client" : "clients"}
              </span>
            ) : null}
          </div>

          {isLoading ? (
            <p role="status" className="mt-5 text-sm text-slate-600">
              Loading clients...
            </p>
          ) : listError ? (
            <div className="mt-5 space-y-3">
              <p role="alert" className="text-sm text-red-700">
                Unable to load clients: {listError}
              </p>
              <button
                className="rounded-md border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
                onClick={() => void loadClients()}
                type="button"
              >
                Try again
              </button>
            </div>
          ) : clients.length === 0 ? (
            <p className="mt-5 rounded-lg border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-600">
              No clients yet. Use the form to create your first client.
            </p>
          ) : (
            <ul className="mt-5 divide-y divide-slate-200">
              {clients.map((client) => (
                <li className="py-4 first:pt-0 last:pb-0" key={client.id}>
                  <Link
                    className="flex flex-col gap-2 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 sm:flex-row sm:items-center sm:justify-between"
                    href={`/clients/${encodeURIComponent(client.id)}`}
                  >
                    <span>
                      <span className="block font-medium text-slate-900">
                        {client.name}
                      </span>
                      <span className="mt-1 block text-sm text-slate-600">
                        {client.email ?? client.phone ?? "No contact details"}
                      </span>
                    </span>
                    <span
                      className={`w-fit rounded-full px-2.5 py-1 text-xs font-semibold capitalize ${
                        client.status === "active"
                          ? "bg-emerald-100 text-emerald-800"
                          : "bg-slate-100 text-slate-700"
                      }`}
                    >
                      {client.status}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section
          aria-labelledby="create-client-heading"
          className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
        >
          <h2
            className="text-lg font-semibold text-slate-900"
            id="create-client-heading"
          >
            Add a client
          </h2>
          <p className="mt-1 text-sm text-slate-600">
            New records are saved to your provider workspace.
          </p>
          {createError ? (
            <p className="mt-4 text-sm text-red-700" role="alert">
              Unable to create client: {createError}
            </p>
          ) : null}
          {notice ? (
            <p className="mt-4 text-sm text-emerald-700" role="status">
              {notice}
            </p>
          ) : null}
          <div className="mt-5">
            <ClientForm
              onSubmit={handleCreate}
              resetOnSuccess
              isSubmitting={isCreating}
              submitLabel="Create client"
            />
          </div>
        </section>
      </div>
    </WorkspaceShell>
  );
}
