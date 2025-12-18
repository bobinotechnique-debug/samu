import { useCallback, useEffect, useState } from "react";

import { buildRequestHeaders } from "../../shared/api/client";

type OrgSummary = {
  id: string;
  name: string;
  is_active: boolean;
  role: string;
};

type OrgDetail = OrgSummary & {
  created_at: string;
  created_by: string | null;
  updated_at: string | null;
  updated_by: string | null;
  request_id: string | null;
};

type MembershipSummary = {
  id: string;
  user_id: string;
  org_id: string;
  role: string;
  created_at: string;
  created_by: string | null;
};

const TOKEN_KEY = "samu-dev-token";
const ORG_KEY = "samu-active-org";
const apiBase = import.meta.env.VITE_API_BASE_URL ?? "";

export const PlaceholderPage = () => {
  const [token, setToken] = useState<string>(() => localStorage.getItem(TOKEN_KEY) ?? "");
  const [orgId, setOrgId] = useState<string>(() => localStorage.getItem(ORG_KEY) ?? "");
  const [orgs, setOrgs] = useState<OrgSummary[]>([]);
  const [memberships, setMemberships] = useState<MembershipSummary[]>([]);
  const [activeOrg, setActiveOrg] = useState<OrgDetail | null>(null);
  const [message, setMessage] = useState<string>("");
  const [error, setError] = useState<string>("");

  useEffect(() => {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
    }
  }, [token]);

  useEffect(() => {
    localStorage.setItem(ORG_KEY, orgId);
  }, [orgId]);

  const headersWithAuth = useCallback(
    (targetOrgId?: string) => {
      const headers = buildRequestHeaders(token, targetOrgId || orgId);
      if (Object.keys(headers).length > 0) {
        headers["Content-Type"] = "application/json";
      }
      return headers;
    },
    [orgId, token]
  );

  const fetchJson = useCallback(
    async (path: string, targetOrg?: string) => {
      setError("");
      const response = await fetch(`${apiBase}${path}`, {
        headers: headersWithAuth(targetOrg),
      });
      const payload = await response.json();
      if (!response.ok) {
        const message = payload?.error?.message ?? "Request failed";
        setError(message);
        throw new Error(message);
      }
      return payload;
    },
    [headersWithAuth]
  );

  const loadOrgs = useCallback(async () => {
    const data = await fetchJson("/orgs");
    setOrgs(data);
  }, [fetchJson]);

  const loadActiveOrg = useCallback(async () => {
    const data: OrgDetail = await fetchJson("/orgs/me");
    setActiveOrg(data);
  }, [fetchJson]);

  const loadMemberships = useCallback(
    async (targetOrgId: string) => {
      const data: MembershipSummary[] = await fetchJson(`/orgs/${targetOrgId}/memberships`, targetOrgId);
      setMemberships(data);
    },
    [fetchJson]
  );

  const handleSelectOrg = async (targetOrgId: string) => {
    setOrgId(targetOrgId);
    await loadMemberships(targetOrgId);
  };

  const handleSaveToken = () => {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(ORG_KEY, orgId);
    setMessage("Token saved for this browser session.");
  };

  return (
    <main className="p-4 space-y-4">
      <header>
        <h1 className="text-xl font-semibold">Org context console</h1>
        <p className="text-sm text-gray-700">Enter a dev token to call the backend slice.</p>
      </header>

      <section className="space-y-2">
        <label className="block text-sm font-medium" htmlFor="token">
          Bearer token
        </label>
        <input
          id="token"
          className="w-full border p-2"
          value={token}
          onChange={(event) => setToken(event.target.value)}
          placeholder="dev-token"
        />
        <label className="block text-sm font-medium" htmlFor="orgId">
          Active org (X-Org-ID)
        </label>
        <input
          id="orgId"
          className="w-full border p-2"
          value={orgId}
          onChange={(event) => setOrgId(event.target.value)}
          placeholder="Organization ID"
        />
        <div className="flex gap-2">
          <button className="rounded bg-blue-600 px-3 py-2 text-white" onClick={handleSaveToken} type="button">
            Save token
          </button>
          <button className="rounded bg-gray-700 px-3 py-2 text-white" onClick={loadActiveOrg} type="button">
            Load active org
          </button>
          <button className="rounded bg-gray-700 px-3 py-2 text-white" onClick={loadOrgs} type="button">
            List my orgs
          </button>
        </div>
        {message && <p className="text-green-700 text-sm">{message}</p>}
        {error && <p className="text-red-700 text-sm">{error}</p>}
      </section>

      <section className="space-y-2">
        <h2 className="text-lg font-semibold">Active org</h2>
        {activeOrg ? (
          <div className="border p-3">
            <p className="font-medium">{activeOrg.name}</p>
            <p className="text-sm">Org ID: {activeOrg.id}</p>
            <p className="text-sm">Role: {activeOrg.role}</p>
            <p className="text-xs">Request: {activeOrg.request_id ?? "n/a"}</p>
          </div>
        ) : (
          <p className="text-sm">No active organization loaded.</p>
        )}
      </section>

      <section className="space-y-2">
        <h2 className="text-lg font-semibold">Organizations</h2>
        {orgs.length === 0 ? (
          <p className="text-sm">No organizations loaded.</p>
        ) : (
          <ul className="space-y-2">
            {orgs.map((org) => (
              <li key={org.id} className="border p-3">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">{org.name}</p>
                    <p className="text-sm">Role: {org.role}</p>
                  </div>
                  <button
                    className="rounded bg-indigo-700 px-3 py-2 text-white"
                    onClick={() => handleSelectOrg(org.id)}
                    type="button"
                  >
                    Use org
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="space-y-2">
        <h2 className="text-lg font-semibold">Memberships</h2>
        {memberships.length === 0 ? (
          <p className="text-sm">No memberships loaded.</p>
        ) : (
          <table className="min-w-full border text-sm">
            <thead>
              <tr>
                <th className="border px-2 py-1 text-left">User</th>
                <th className="border px-2 py-1 text-left">Role</th>
              </tr>
            </thead>
            <tbody>
              {memberships.map((membership) => (
                <tr key={membership.id}>
                  <td className="border px-2 py-1">{membership.user_id}</td>
                  <td className="border px-2 py-1">{membership.role}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
};
