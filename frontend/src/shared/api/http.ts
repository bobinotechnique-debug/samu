import { ApiErrorPayload, ApiErrorResponse } from "./errors";
import { apiBaseUrl, apiVersionPath } from "./versioning";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export type RequestOptions = {
  method?: HttpMethod;
  headers?: Record<string, string>;
  body?: unknown;
  signal?: AbortSignal;
  timeoutMs?: number;
  versioned?: boolean;
};

const DEFAULT_TIMEOUT_MS = 5000;

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = apiBaseUrl) {
    this.baseUrl = baseUrl;
  }

  buildUrl(path: string, versioned: boolean = true): string {
    const normalizedPath = path.startsWith("/") ? path : `/${path}`;
    const prefix = versioned ? apiVersionPath : "";
    return `${this.baseUrl}${prefix}${normalizedPath}`;
  }

  async request<T = unknown>(path: string, options: RequestOptions = {}): Promise<T> {
    const controller = new AbortController();
    const timeout = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;
    const timer = setTimeout(() => controller.abort(), timeout);

    const response = await fetch(this.buildUrl(path, options.versioned ?? true), {
      method: options.method ?? "GET",
      headers: {
        Accept: "application/json",
        ...(options.body ? { "Content-Type": "application/json" } : {}),
        ...options.headers,
      },
      body: options.body ? JSON.stringify(options.body) : undefined,
      signal: options.signal ?? controller.signal,
    });

    clearTimeout(timer);

    if (!response.ok) {
      let payload: ApiErrorPayload = { code: "http_error", message: "Request failed" };
      try {
        const data = await response.json();
        if (data?.error?.code && data?.error?.message) {
          payload = {
            code: data.error.code,
            message: data.error.message,
            details: data.error.details,
            request_id: data.error.request_id,
            timestamp: data.error.timestamp,
          };
        }
      } catch {
        // swallow JSON parse errors and return default payload
      }
      throw new ApiErrorResponse(response.status, payload);
    }

    if (response.status === 204) {
      return null as T;
    }

    return (await response.json()) as T;
  }
}
