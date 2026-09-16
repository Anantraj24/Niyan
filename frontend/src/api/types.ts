export interface HealthResponse {
  status: string;
  api_version: string;
  solver_available: boolean;
  verifier_available: boolean;
}

export interface CPUInfo {
  name: string;
  logical_cores: number;
  system_ram_bytes: number;
}

export interface GPUInfo {
  cuda_available: boolean;
  name: string;
  vram_bytes: number;
}

export interface HardwareResponse {
  cpu: CPUInfo;
  gpu: GPUInfo;
}

export interface ModelSummary {
  model_id: string;
  display_name: string;
  dataset_kind: string;
  current_version_id?: string;
  created_at: string;
  updated_at: string;
  version_count: number;
}

export interface ModelVersionSummary {
  version_id: string;
  format: string;
  sha256: string;
  size_bytes: number;
  created_at: string;
}

export interface ModelDetail {
  model_id: string;
  display_name: string;
  dataset_kind: string;
  current_version?: ModelVersionSummary;
  created_at: string;
  updated_at: string;
}

export interface ProfileData {
  variables: number;
  constraints: number;
  nonzeros: number;
  density: number;
  coefficient_min_abs: number;
  coefficient_max_abs: number;
  coefficient_dynamic_range: number;
  integer_ratio: number;
  binary_ratio: number;
  fixed_variables: number;
  singleton_rows: number;
}

export interface RiskIssue {
  code: string;
  severity: "LOW" | "MEDIUM" | "HIGH";
  message: string;
}

export interface RiskData {
  level: "LOW" | "MEDIUM" | "HIGH";
  issues: RiskIssue[];
}

export interface AutopilotData {
  backend: string;
  scaling: string;
  warm_start_eligible: boolean;
  reasons: string[];
}

export interface AnalysisResponse {
  analysis_id: string;
  model_id: string;
  version_id: string;
  profile: ProfileData;
  risk: RiskData;
  autopilot: AutopilotData;
}

export interface SolveConfig {
  backend?: string;
  scaling?: string;
  time_limit_sec?: number;
  iteration_limit?: number;
  tolerance?: number;
}

export interface CreateSolveResponse {
  solve_id: string;
  state: string;
  events_url: string;
}

export interface SolveStatusResponse {
  solve_id: string;
  model_id: string;
  version_id: string;
  parent_solve_id?: string;
  state: string;
  solver_status?: string;
  backend?: string;
  scaling?: string;
  warm_start: boolean;
  objective?: number;
  iterations?: number;
  solve_time_ms?: number;
  primal_residual?: number;
  dual_residual?: number;
  verification_state: string;
  verification_verdict?: string;
  error_code?: string;
  error_message?: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
}

export interface VerificationResponse {
  verification_id: string;
  solve_id: string;
  state: string;
  verdict?: "VERIFIED" | "VERIFICATION_FAILED";
  max_primal_violation?: number;
  max_bound_violation?: number;
  max_integrality_violation?: number;
  objective_error?: number;
  model_hash_match?: boolean;
  error_message?: string;
  created_at: string;
  completed_at?: string;
}

export interface BenchmarkResultItem {
  solver: string;
  backend?: string;
  model_id?: string;
  valid: boolean;
  runtime_ms?: number;
  objective?: number;
  primal_residual?: number;
  dual_residual?: number;
  solver_status?: string;
}

export interface BenchmarkResponse {
  benchmark_id: string;
  state: string;
  results: BenchmarkResultItem[];
  created_at: string;
  completed_at?: string;
}
