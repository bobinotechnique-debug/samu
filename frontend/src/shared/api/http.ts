import { loadEnv } from "./config";

export const apiVersionPath = "/api/v1";
const { apiBaseUrl: rawApiBaseUrl } = loadEnv();
const normalizeBaseUrl = (value: string) => value.replace(/\/+$/, "");
const ensurePath = (path: string) => (path.startsWith("/") ? path : `/${path}`);
const normalizedVersionPath = apiVersionPath.replace(/\/+$/, "");

export const apiBaseUrl = normalizeBaseUrl(rawApiBaseUrl);

export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export type ApiErrorContent = {
  code: string;
  message: string;
  details?: unknown;
  request_id?: string;
  timestamp?: string;
};

export type ApiErrorResponse = {
  error: ApiErrorContent;
};

export type RequestOptions = {
  path: string;
  method?: HttpMethod;
  headers?: Record<string, string>;
  body?: unknown;
  timeoutMs?: number;
  signal?: AbortSignal;
  versioned?: boolean;
};

export class ApiError extends Error {
  status: number;
  payload: ApiErrorContent;

  constructor(status: number, payload: ApiErrorContent) {
    super(payload.message);
    this.name = "ApiError";
    this.status = status;
    this.payload = payload;
  }
}

const buildUrl = (path: string, versioned: boolean) => {
  const normalizedPath = ensurePath(path);
  const baseAlreadyVersioned = apiBaseUrl.endsWith(normalizedVersionPath);
  if (!versioned) {
    return `${apiBaseUrl}${normalizedPath}`;
  }
  const baseForRequest = baseAlreadyVersioned ? apiBaseUrl : `${apiBaseUrl}${normalizedVersionPath}`;
  return `${baseForRequest}${normalizedPath}`;
};

const parseError = async (response: Response): Promise<ApiErrorContent> => {
  try {
    const data = (await response.json()) as ApiErrorResponse;
    if (data?.error?.code && data?.error?.message) {
      return {
        code: data.error.code,
        message: data.error.message,
        details: data.error.details ?? {},
        request_id: data.error.request_id,
        timestamp: data.error.timestamp,
      };
    }
  } catch {
    // fall through to default payload
  }

  return {
    code: "http_error",
    message: `Request failed with status ${response.status}`,
    details: {},
  };
};

export const request = async <T>({
  path,
  method = "GET",
  headers,
  body,
  timeoutMs = 10000,
  signal,
  versioned = true,
}: RequestOptions): Promise<T> => {
  const controller = signal ? null : new AbortController();
  const abortSignal = signal ?? controller?.signal;
  const timer = controller ? setTimeout(() => controller.abort(), timeoutMs) : null;

  const requestInit: RequestInit = {
    method,
    headers: {
      ...(headers ?? {}),
    },
    signal: abortSignal,
  };

  if (body !== undefined) {
    requestInit.body = JSON.stringify(body);
    requestInit.headers = {
      "Content-Type": "application/json",
      ...(headers ?? {}),
    };
  }

  try {
    const response = await fetch(buildUrl(path, versioned), requestInit);
    if (!response.ok) {
      throw new ApiError(response.status, await parseError(response));
    }
    if (response.status === 204) {
      return undefined as T;
    }
    return (await response.json()) as T;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError(0, { code: "request.aborted", message: "Request aborted", details: {} });
    }
    throw error;
  } finally {
    if (timer) {
      clearTimeout(timer);
    }
  }
};
