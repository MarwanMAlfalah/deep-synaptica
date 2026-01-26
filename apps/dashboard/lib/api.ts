const BASE = process.env.NEXT_PUBLIC_API_BASE;

if (!BASE) {
  throw new Error("NEXT_PUBLIC_API_BASE is not set");
}

export async function getRuns() {
  const res = await fetch(`${BASE}/runs`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to fetch runs: ${res.status}`);
  return res.json();
}

export async function getRun(runId: string) {
  const res = await fetch(`${BASE}/runs/${encodeURIComponent(runId)}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to fetch run: ${res.status}`);
  return res.json();
}
