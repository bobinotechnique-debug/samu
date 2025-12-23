import { afterEach, beforeEach, expect, it, vi } from "vitest";

import { ApiClient } from "../http";
import { ApiErrorResponse } from "../errors";

const createResponse = (body: object, init?: ResponseInit) =>
  new Response(JSON.stringify(body), { status: 200, headers: { "Content-Type": "application/json" }, ...init });

describe("ApiClient", () => {
  const originalFetch = global.fetch;

  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    global.fetch = originalFetch;
    vi.clearAllMocks();
  });

  it("builds versioned url and parses JSON payload", async () => {
    const client = new ApiClient("http://localhost");
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce(createResponse({ status: "ok" }));

    const result = await client.request<{ status: string }>("/health", { versioned: false });

    expect(result.status).toBe("ok");
    expect(global.fetch).toHaveBeenCalledWith(
      "http://localhost/health",
      expect.objectContaining({ method: "GET" })
    );
  });

  it("throws ApiErrorResponse on HTTP errors with mapped payload", async () => {
    const client = new ApiClient("http://localhost");
    const errorResponse = { error: { code: "internal_error", message: "failed", request_id: "req-123" } };
    (global.fetch as unknown as ReturnType<typeof vi.fn>).mockResolvedValueOnce(
      createResponse(errorResponse, { status: 500 })
    );

    await expect(client.request("/health", { versioned: false })).rejects.toBeInstanceOf(ApiErrorResponse);
  });
});
