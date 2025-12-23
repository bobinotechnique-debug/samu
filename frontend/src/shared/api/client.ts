export type ApiHeaders = Record<string, string>;

export const buildRequestHeaders = (token: string, orgId?: string): ApiHeaders => {
  const headers: ApiHeaders = {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  if (orgId) {
    headers["X-Org-ID"] = orgId;
  }
  return headers;
};
