import { describe, expect, it } from "vitest";

import { buildRequestHeaders } from "./client";


describe("buildRequestHeaders", () => {
  it("includes authorization and org headers when provided", () => {
    const headers = buildRequestHeaders("token-123", "org-456");

    expect(headers.Authorization).toBe("Bearer token-123");
    expect(headers["X-Org-ID"]).toBe("org-456");
  });

  it("omits headers when values are empty", () => {
    const headers = buildRequestHeaders("", undefined);

    expect(headers.Authorization).toBeUndefined();
    expect(headers["X-Org-ID"]).toBeUndefined();
  });
});
