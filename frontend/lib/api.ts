export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type ApiErrorPayload = {
  error?: { message?: string };
  detail?: string;
};

export async function apiRequest<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const headers = new Headers(init.headers);
  if (init.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    credentials: "include",
    headers,
  });
  const responseText = await response.text();

  let payload: T | ApiErrorPayload;
  try {
    payload = JSON.parse(responseText) as T | ApiErrorPayload;
  } catch {
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}.`);
    }
    throw new Error("The server returned an invalid JSON response.");
  }

  if (!response.ok) {
    const errorPayload = payload as ApiErrorPayload;
    throw new Error(
      errorPayload.error?.message ??
        errorPayload.detail ??
        `Request failed with status ${response.status}.`,
    );
  }

  return payload as T;
}

export type ProviderProfile = {
  id: string;
  name: string;
  business_name: string | null;
  timezone: string;
  tone: string | null;
  modality: string | null;
  service_type: string | null;
  template_settings: Record<string, unknown> | null;
  boundaries: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
};

export type ProviderProfileUpdate = Pick<
  ProviderProfile,
  "name" | "business_name" | "timezone"
>;

export type ClientStatus = "active" | "inactive";

export type ClientRecord = {
  id: string;
  provider_id: string;
  name: string;
  email: string | null;
  phone: string | null;
  timezone: string;
  service_type: string | null;
  goals: string[];
  status: ClientStatus;
  created_at: string;
  updated_at: string;
};

export type ClientWrite = {
  name: string;
  email: string | null;
  phone: string | null;
  timezone: string;
  service_type: string | null;
  goals: string[];
  status: ClientStatus;
};

export async function fetchProviderProfile(): Promise<ProviderProfile> {
  return apiRequest<ProviderProfile>("/api/v1/providers/me");
}

export async function updateProviderProfile(
  profile: ProviderProfileUpdate,
): Promise<ProviderProfile> {
  return apiRequest<ProviderProfile>("/api/v1/providers/me", {
    method: "PATCH",
    body: JSON.stringify(profile),
  });
}

export async function fetchClients(): Promise<ClientRecord[]> {
  return apiRequest<ClientRecord[]>("/api/v1/clients");
}

export async function createClient(client: ClientWrite): Promise<ClientRecord> {
  return apiRequest<ClientRecord>("/api/v1/clients", {
    method: "POST",
    body: JSON.stringify(client),
  });
}

export async function fetchClient(clientId: string): Promise<ClientRecord> {
  return apiRequest<ClientRecord>(
    `/api/v1/clients/${encodeURIComponent(clientId)}`,
  );
}

export async function updateClient(
  clientId: string,
  client: ClientWrite,
): Promise<ClientRecord> {
  return apiRequest<ClientRecord>(
    `/api/v1/clients/${encodeURIComponent(clientId)}`,
    {
      method: "PATCH",
      body: JSON.stringify(client),
    },
  );
}

export async function fetchJson<T>(path: string): Promise<T> {
  return apiRequest<T>(path);
}
