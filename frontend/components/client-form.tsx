"use client";

import { useState, type FormEvent } from "react";

import type { ClientStatus, ClientWrite } from "@/lib/api";

export type ClientFormValues = {
  name: string;
  email: string;
  phone: string;
  timezone: string;
  service_type: string;
  goals: string;
  status: ClientStatus;
};

const EMPTY_VALUES: ClientFormValues = {
  name: "",
  email: "",
  phone: "",
  timezone: "UTC",
  service_type: "",
  goals: "",
  status: "active",
};

function normalizeClientValues(values: ClientFormValues): ClientWrite {
  return {
    name: values.name.trim(),
    email: values.email.trim() || null,
    phone: values.phone.trim() || null,
    timezone: values.timezone.trim(),
    service_type: values.service_type.trim() || null,
    goals: values.goals
      .split("\n")
      .map((goal) => goal.trim())
      .filter(Boolean),
    status: values.status,
  };
}

export function ClientForm({
  initialValues = EMPTY_VALUES,
  submitLabel,
  isSubmitting,
  resetOnSuccess = false,
  onSubmit,
}: {
  initialValues?: ClientFormValues;
  submitLabel: string;
  isSubmitting: boolean;
  resetOnSuccess?: boolean;
  onSubmit: (values: ClientWrite) => Promise<boolean | void>;
}) {
  const [values, setValues] = useState(initialValues);

  function setField<K extends keyof ClientFormValues>(
    field: K,
    value: ClientFormValues[K],
  ) {
    setValues((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const succeeded = await onSubmit(normalizeClientValues(values));
    if (resetOnSuccess && succeeded !== false) {
      setValues(EMPTY_VALUES);
    }
  }

  const inputClassName =
    "mt-1 block w-full rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-900 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200";

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <label className="block text-sm font-medium text-slate-700">
        Name
        <input
          autoComplete="name"
          className={inputClassName}
          maxLength={255}
          onChange={(event) => setField("name", event.target.value)}
          required
          value={values.name}
        />
      </label>

      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block text-sm font-medium text-slate-700">
          Email
          <input
            autoComplete="email"
            className={inputClassName}
            maxLength={320}
            onChange={(event) => setField("email", event.target.value)}
            type="email"
            value={values.email}
          />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          Phone
          <input
            autoComplete="tel"
            className={inputClassName}
            maxLength={32}
            onChange={(event) => setField("phone", event.target.value)}
            value={values.phone}
          />
        </label>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block text-sm font-medium text-slate-700">
          Timezone
          <input
            className={inputClassName}
            maxLength={64}
            onChange={(event) => setField("timezone", event.target.value)}
            required
            value={values.timezone}
          />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          Service type
          <input
            className={inputClassName}
            maxLength={100}
            onChange={(event) => setField("service_type", event.target.value)}
            value={values.service_type}
          />
        </label>
      </div>

      <label className="block text-sm font-medium text-slate-700">
        Goals
        <textarea
          className={inputClassName}
          onChange={(event) => setField("goals", event.target.value)}
          placeholder="Enter one goal per line"
          rows={3}
          value={values.goals}
        />
      </label>

      <label className="block text-sm font-medium text-slate-700">
        Status
        <select
          className={inputClassName}
          onChange={(event) => {
            const status = event.target.value;
            if (status === "active" || status === "inactive") {
              setField("status", status);
            }
          }}
          value={values.status}
        >
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </label>

      <button
        className="inline-flex items-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-300"
        disabled={isSubmitting}
        type="submit"
      >
        {isSubmitting ? "Saving..." : submitLabel}
      </button>
    </form>
  );
}
