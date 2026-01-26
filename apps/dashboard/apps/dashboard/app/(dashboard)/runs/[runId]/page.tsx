import { getRun } from "@/lib/api";

type Props = { params: Promise<{ runId: string }> };

export default async function RunDetails({ params }: Props) {
  const { runId } = await params;
  const data = await getRun(runId);

  const run = data.run;
  const steps = data.steps ?? [];

  return (
    <main style={{ padding: 24 }}>
      <h1 style={{ fontSize: 28, fontWeight: 800 }}>Run Details</h1>

      <p><b>ID:</b> {run.run_id}</p>
      <p><b>Status:</b> {run.status}</p>
      <p><b>Latency:</b> {run.total_latency_ms} ms</p>
      <p><b>Steps:</b> {run.step_count}</p>

      <h2 style={{ marginTop: 24 }}>Steps</h2>
      <pre style={{ whiteSpace: "pre-wrap", opacity: 0.9 }}>
        {JSON.stringify(steps, null, 2)}
      </pre>
    </main>
  );
}
