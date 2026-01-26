import Link from "next/link";
import { getRuns } from "@/lib/api";

export default async function RunsPage() {
  const data = await getRuns();
  const runs = data.runs || [];

  return (
    <main style={{ padding: 24 }}>
      <h1 style={{ fontSize: 28, fontWeight: 800 }}>Runs</h1>
      <p style={{ opacity: 0.7 }}>Total: {data.count}</p>

      <div style={{ marginTop: 16, display: "grid", gap: 12 }}>
        {runs.map((r: any) => (
          <Link
            key={r.run_id}
            href={`/runs/${r.run_id}`}
            style={{
              border: "1px solid #2b2b2b",
              borderRadius: 14,
              padding: 16,
              textDecoration: "none",
              color: "inherit",
              display: "block",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <strong>{r.run_id}</strong>
              <span>{r.status}</span>
            </div>

            <div style={{ marginTop: 8, opacity: 0.85 }}>
              steps: {r.step_count} · latency: {r.total_latency_ms}ms · v: {r.agent_version}
            </div>

            <div style={{ marginTop: 6, opacity: 0.6, fontSize: 12 }}>
              {String(r.created_at)}
            </div>
          </Link>
        ))}
      </div>
    </main>
  );
}
