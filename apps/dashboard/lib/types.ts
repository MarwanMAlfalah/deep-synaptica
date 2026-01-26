export type RunSummary = {
  run_id: string;
  agent_version: string;
  created_at: string;
  step_count: number;
  total_latency_ms: number;
  status: "SUCCESS" | "FAIL";
  trace_file: string;
};

export type Step = {
  run_id: string;
  agent_version: string;
  step_type: string;
  prompt: string;
  response: string;
  latency_ms?: number;
  meta?: Record<string, any>;
  error?: string | null;
  created_at: string;
};
