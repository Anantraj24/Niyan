import type {
  HealthResponse,
  HardwareResponse,
  ModelSummary,
  ModelDetail,
  AnalysisResponse,
  SolveConfig,
  CreateSolveResponse,
  SolveStatusResponse,
  VerificationResponse,
  BenchmarkResponse
} from './types';

const BASE_URL = '/api/v1';

export async function getHealth(): Promise<HealthResponse> {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) throw new Error('Failed to fetch health');
  return res.json();
}

export async function getHardware(): Promise<HardwareResponse> {
  const res = await fetch(`${BASE_URL}/hardware`);
  if (!res.ok) throw new Error('Failed to fetch hardware');
  return res.json();
}

export async function getModels(): Promise<ModelSummary[]> {
  const res = await fetch(`${BASE_URL}/models`);
  if (!res.ok) throw new Error('Failed to fetch models');
  return res.json();
}

export async function getModel(modelId: string): Promise<ModelDetail> {
  const res = await fetch(`${BASE_URL}/models/${modelId}`);
  if (!res.ok) throw new Error('Failed to fetch model');
  return res.json();
}

export async function analyzeModel(modelId: string, versionId?: string): Promise<AnalysisResponse> {
  const res = await fetch(`${BASE_URL}/models/${modelId}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(versionId ? { version_id: versionId } : {})
  });
  if (!res.ok) throw new Error('Failed to run Model X-Ray');
  return res.json();
}

export async function getLatestAnalysis(modelId: string): Promise<AnalysisResponse> {
  const res = await fetch(`${BASE_URL}/models/${modelId}/analysis`);
  if (!res.ok) throw new Error('Failed to fetch analysis');
  return res.json();
}

export async function createSolve(
  modelId: string,
  config?: SolveConfig,
  versionId?: string
): Promise<CreateSolveResponse> {
  const res = await fetch(`${BASE_URL}/solves`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model_id: modelId,
      version_id: versionId,
      config: config || {}
    })
  });
  if (!res.ok) throw new Error('Failed to create solve');
  return res.json();
}

export async function getSolveStatus(solveId: string): Promise<SolveStatusResponse> {
  const res = await fetch(`${BASE_URL}/solves/${solveId}`);
  if (!res.ok) throw new Error('Failed to fetch solve status');
  return res.json();
}

export async function resolveDelta(
  parentSolveId: string,
  changes: Record<string, any>,
  config?: SolveConfig
): Promise<CreateSolveResponse> {
  const res = await fetch(`${BASE_URL}/solves/${parentSolveId}/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      changes,
      config
    })
  });
  if (!res.ok) throw new Error('Failed to resolve DeltaSolve');
  return res.json();
}

export async function verifySolve(solveId: string): Promise<VerificationResponse> {
  const res = await fetch(`${BASE_URL}/solves/${solveId}/verify`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Failed to verify solve');
  return res.json();
}

export async function getVerification(solveId: string): Promise<VerificationResponse> {
  const res = await fetch(`${BASE_URL}/solves/${solveId}/verification`);
  if (!res.ok) throw new Error('Failed to fetch verification');
  return res.json();
}

export async function runBenchmark(modelIds: string[], backends: string[] = ['CPU', 'CUDA']): Promise<BenchmarkResponse> {
  const res = await fetch(`${BASE_URL}/benchmarks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model_ids: modelIds,
      backends,
      include_reference: false
    })
  });
  if (!res.ok) throw new Error('Failed to run benchmark');
  return res.json();
}
