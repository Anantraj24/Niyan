import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import type { TabKey } from './components/Sidebar';
import { Footer } from './components/Footer';
import { ModelOverviewView } from './features/ModelOverviewView';
import { ModelXRayView } from './features/ModelXRayView';
import { AutopilotView } from './features/AutopilotView';
import { SolveTelemetryView } from './features/SolveTelemetryView';
import { DeltaSolveView } from './features/DeltaSolveView';
import { ProofPackView } from './features/ProofPackView';
import { BenchmarkView } from './features/BenchmarkView';
import {
  getHealth,
  getHardware,
  getModels,
  getModel,
  analyzeModel,
  getLatestAnalysis,
  createSolve,
  getSolveStatus,
  resolveDelta,
  verifySolve,
  runBenchmark
} from './api/client';
import type {
  HealthResponse,
  HardwareResponse,
  ModelSummary,
  ModelDetail,
  AnalysisResponse,
  SolveStatusResponse,
  VerificationResponse,
  BenchmarkResponse,
  SolveConfig
} from './api/types';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabKey>('overview');
  const [models, setModels] = useState<ModelSummary[]>([]);
  const [selectedModelId, setSelectedModelId] = useState<string>('');
  const [modelDetail, setModelDetail] = useState<ModelDetail | undefined>();
  const [analysis, setAnalysis] = useState<AnalysisResponse | undefined>();
  const [hardware, setHardware] = useState<HardwareResponse | undefined>();
  const [health, setHealth] = useState<HealthResponse | undefined>();

  // Solves State
  const [activeSolve, setActiveSolve] = useState<SolveStatusResponse | undefined>();
  const [baselineSolve, setBaselineSolve] = useState<SolveStatusResponse | undefined>();
  const [deltaSolve, setDeltaSolve] = useState<SolveStatusResponse | undefined>();
  const [verification, setVerification] = useState<VerificationResponse | undefined>();
  const [benchmark, setBenchmark] = useState<BenchmarkResponse | undefined>();
  const [telemetryHistory, setTelemetryHistory] = useState<any[]>([]);

  // Loading flags
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isSolving, setIsSolving] = useState(false);
  const [isResolving, setIsResolving] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [isRunningBenchmark, setIsRunningBenchmark] = useState(false);

  // Initial Load: Health, Hardware, and Models
  useEffect(() => {
    async function init() {
      try {
        const [h, hw, mList] = await Promise.all([getHealth(), getHardware(), getModels()]);
        setHealth(h);
        setHardware(hw);
        setModels(mList);

        if (mList.length > 0) {
          const defaultId = mList[0].model_id;
          setSelectedModelId(defaultId);
        }
      } catch (err) {
        console.error('Initialization error:', err);
      }
    }
    init();
  }, []);

  // When selectedModelId changes, load model detail and latest analysis
  useEffect(() => {
    if (!selectedModelId) return;

    async function loadModelData() {
      try {
        const detail = await getModel(selectedModelId);
        setModelDetail(detail);

        try {
          const ana = await getLatestAnalysis(selectedModelId);
          setAnalysis(ana);
        } catch {
          // If no analysis exists yet, automatically run initial Model X-Ray
          handleRunXRay();
        }
      } catch (err) {
        console.error('Error loading model detail:', err);
      }
    }
    loadModelData();
  }, [selectedModelId]);

  // Handler: Model Imported via UI
  const handleModelImported = async (newModelId: string) => {
    try {
      const mList = await getModels();
      setModels(mList);
      setSelectedModelId(newModelId);
    } catch (err) {
      console.error('Failed to reload models after import:', err);
    }
  };

  // Handler: Run Model X-Ray
  const handleRunXRay = async () => {
    if (!selectedModelId) return;
    setIsAnalyzing(true);
    try {
      const res = await analyzeModel(selectedModelId);
      setAnalysis(res);
    } catch (err) {
      console.error('Analysis error:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Handler: Start Solve & Stream SSE Telemetry
  const handleExecuteSolve = async (config?: SolveConfig) => {
    if (!selectedModelId) return;
    setIsSolving(true);
    setTelemetryHistory([]);
    setVerification(undefined);

    try {
      const created = await createSolve(selectedModelId, config);
      setActiveTab('solve');

      // Listen for SSE Events
      const eventSource = new EventSource(`/api/v1/solves/${created.solve_id}/events`);

      eventSource.addEventListener('solver.iteration', (e: MessageEvent) => {
        try {
          const data = JSON.parse(e.data);
          setTelemetryHistory((prev) => [
            ...prev,
            {
              iteration: data.iteration,
              primal_residual: data.primal_residual,
              dual_residual: data.dual_residual,
              objective: data.objective
            }
          ]);
        } catch (err) {
          console.error('SSE parse error:', err);
        }
      });

      eventSource.addEventListener('solver.completed', async () => {
        eventSource.close();
        setIsSolving(false);
        const finalStatus = await getSolveStatus(created.solve_id);
        setActiveSolve(finalStatus);
        setBaselineSolve(finalStatus);

        // Automatically trigger independent verification
        handleVerify(created.solve_id);
      });

      eventSource.onerror = async () => {
        eventSource.close();
        setIsSolving(false);
        const st = await getSolveStatus(created.solve_id);
        setActiveSolve(st);
      };
    } catch (err) {
      console.error('Solve error:', err);
      setIsSolving(false);
    }
  };

  // Handler: Verify Solve
  const handleVerify = async (solveIdToVerify?: string) => {
    const sId = solveIdToVerify || activeSolve?.solve_id;
    if (!sId) return;

    setIsVerifying(true);
    try {
      const res = await verifySolve(sId);
      setVerification(res);
    } catch (err) {
      console.error('Verification error:', err);
    } finally {
      setIsVerifying(false);
    }
  };

  // Handler: DeltaSolve Re-solve
  const handleExecuteDeltaSolve = async (changes: Record<string, any>) => {
    if (!baselineSolve) return;
    setIsResolving(true);

    try {
      const res = await resolveDelta(baselineSolve.solve_id, changes);
      
      // Wait for child solve completion
      for (let i = 0; i < 40; i++) {
        await new Promise((r) => setTimeout(r, 100));
        const st = await getSolveStatus(res.solve_id);
        if (st.state === 'COMPLETED' || st.state === 'FAILED') {
          setDeltaSolve(st);
          setActiveSolve(st);
          break;
        }
      }
    } catch (err) {
      console.error('DeltaSolve error:', err);
    } finally {
      setIsResolving(false);
    }
  };

  // Handler: Run Benchmark
  const handleRunBenchmark = async () => {
    if (!selectedModelId) return;
    setIsRunningBenchmark(true);
    try {
      const res = await runBenchmark([selectedModelId], ['CPU', 'CUDA']);
      setBenchmark(res);
    } catch (err) {
      console.error('Benchmark error:', err);
    } finally {
      setIsRunningBenchmark(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0e14] text-slate-100 flex flex-col font-sans">
      {/* Top Header */}
      <Header
        models={models}
        selectedModelId={selectedModelId}
        onSelectModel={setSelectedModelId}
        hardware={hardware}
        health={health}
        onQuickSolve={() => handleExecuteSolve()}
        isSolving={isSolving}
      />

      {/* Main Workspace Layout (Sidebar + Content Panel) */}
      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          activeTab={activeTab}
          onTabChange={setActiveTab}
          solveStatus={activeSolve?.solver_status || activeSolve?.state}
          hasVerification={verification?.verdict === 'VERIFIED'}
        />

        <main className="flex-1 overflow-y-auto bg-[#0b0e14]">
          {activeTab === 'overview' && (
            <ModelOverviewView
              model={modelDetail}
              analysis={analysis}
              onRunXRay={handleRunXRay}
              onGoToAutopilot={() => setActiveTab('autopilot')}
              onGoToSolve={() => setActiveTab('solve')}
              onModelImported={handleModelImported}
              isAnalyzing={isAnalyzing}
            />
          )}

          {activeTab === 'xray' && (
            <ModelXRayView
              analysis={analysis}
              onRunXRay={handleRunXRay}
              onGoToAutopilot={() => setActiveTab('autopilot')}
              isAnalyzing={isAnalyzing}
            />
          )}

          {activeTab === 'autopilot' && (
            <AutopilotView
              analysis={analysis}
              onExecuteSolve={handleExecuteSolve}
              isSolving={isSolving}
            />
          )}

          {activeTab === 'solve' && (
            <SolveTelemetryView
              activeSolve={activeSolve}
              telemetryHistory={telemetryHistory}
              verification={verification}
              onVerify={() => handleVerify()}
              onGoToDelta={() => setActiveTab('delta')}
              isVerifying={isVerifying}
            />
          )}

          {activeTab === 'delta' && (
            <DeltaSolveView
              baselineSolve={baselineSolve}
              deltaSolve={deltaSolve}
              onExecuteDeltaSolve={handleExecuteDeltaSolve}
              isResolving={isResolving}
            />
          )}

          {activeTab === 'proof' && (
            <ProofPackView
              verification={verification}
              activeSolve={activeSolve}
              onVerify={() => handleVerify()}
              isVerifying={isVerifying}
            />
          )}

          {activeTab === 'benchmarks' && (
            <BenchmarkView
              benchmark={benchmark}
              onRunBenchmark={handleRunBenchmark}
              isRunningBenchmark={isRunningBenchmark}
            />
          )}
        </main>
      </div>

      {/* Bottom Status Strip */}
      <Footer health={health} hardware={hardware} activeSolve={activeSolve} />
    </div>
  );
};

export default App;
