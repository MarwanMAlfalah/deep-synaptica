import { getRun } from "@/lib/api";

export default async function RunDetails({
  params,
}: {
  params: { runId: string };
}) {
  const data = await getRun(params.runId);
  const steps = data.steps || [];

  return (
    <main style={{ padding: 24 }}>
      <h1>Run Details</h1>
      <div><b>ID:</b> {data.run_id}</div>
      <div><b>Status:</b> {data.status}</div>
      <div><b>Latency:</b> {data.latency_ms} ms</div>
      <div><b>Steps:</b> {steps.length}</div>

      <h2 style={{ marginTop: 24 }}>Steps</h2>
      <pre style={{ whiteSpace: "pre-wrap" }}>
        {JSON.stringify(steps, null, 2)}
      </pre>
    </main>
  );
}
