export type ClientSession = {
  providerId: string;
  providerName: string;
  businessName?: string;
};

const SESSION_KEY = "ai_pa_session";
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export function getStoredSession(): ClientSession | null {
  if (typeof window === "undefined") return null;

  const raw = window.localStorage.getItem(SESSION_KEY);
  if (!raw) return null;

  try {
    const session = JSON.parse(raw) as ClientSession;
    if (!session.providerId || !session.providerName) {
      return null;
    }
    return session;
  } catch {
    return null;
  }
}

export function setStoredSession(session: ClientSession) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function clearStoredSession() {
  if (typeof window === "undefined") return;
  window.localStorage.removeItem(SESSION_KEY);
}

async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(init.headers ?? {}),
    },
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload?.error?.message ?? "Request failed.");
  }

  return payload as T;
}

export async function loginToDemoProvider(): Promise<ClientSession> {
  const payload = await apiRequest<{ provider_id: string; provider: { name: string; business_name?: string } }>(
    "/api/v1/auth/login",
    {
      method: "POST",
      body: JSON.stringify({ provider_id: "demo-provider" }),
    },
  );

  const session: ClientSession = {
    providerId: payload.provider_id,
    providerName: payload.provider.name,
    businessName: payload.provider.business_name,
  };

  setStoredSession(session);
  return session;
}

export async function logoutFromDemoProvider() {
  await apiRequest<{ status: string }>("/api/v1/auth/logout", { method: "POST" });
  clearStoredSession();
}

export async function fetchCurrentProvider(): Promise<ClientSession | null> {
  try {
    const payload = await apiRequest<{ provider_id: string; provider: { name: string; business_name?: string } }>(
      "/api/v1/auth/me",
      { method: "GET" },
    );

    const session: ClientSession = {
      providerId: payload.provider_id,
      providerName: payload.provider.name,
      businessName: payload.provider.business_name,
    };

    setStoredSession(session);
    return session;
  } catch {
    clearStoredSession();
    return null;
  }
}
