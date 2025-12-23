import { afterEach, describe, expect, it, vi } from "vitest";

const originalFetch = globalThis.fetch;

describe("http request wrapper", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.resetModules();
    vi.unstubAllEnvs();
    (globalThis as unknown as { fetch: typeof fetch }).fetch = originalFetch;
  });

  it("builds non-versioned URLs when requested", async () => {
    vi.stubEnv("VITE_API_BASE_URL", "http://example.com");
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ status: "ok" }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      })
    );
    (globalThis as unknown as { fetch: typeof fetch }).fetch = fetchMock;

    const { request } = await import("./http");

    await request({ path: "/health", versioned: false });

    expect(fetchMock).toHaveBeenCalledWith(
      "http://example.com/health",
      expect.objectContaining({ method: "GET" })
    );
  });

  it("throws ApiError with mapped payload on non-2xx responses", async () => {
    vi.stubEnv("VITE_API_BASE_URL", "http://example.com");
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(
        JSON.stringify({
          error: {
            code: "validation_error",
            message: "Invalid payload",
            details: { field: "name" },
            request_id: "req-123",
            timestamp: "2024-01-01T00:00:00Z",
          },
        }),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        }
      )
    );
    (globalThis as unknown as { fetch: typeof fetch }).fetch = fetchMock;

    const { ApiError, request } = await import("./http");
    const requestPromise = request({ path: "/health", versioned: false });

    await expect(requestPromise).rejects.toBeInstanceOf(ApiError);
    await expect(requestPromise).rejects.toMatchObject({
      status: 400,
      payload: {
        code: "validation_error",
        message: "Invalid payload",
        details: { field: "name" },
        request_id: "req-123",
        timestamp: "2024-01-01T00:00:00Z",
      },
    });
  });
});
