import React from 'react';
import { Layers, Shield, Zap, RefreshCw, CheckCircle2 } from 'lucide-react';
import type { ModelDetail, AnalysisResponse } from '../api/types';
import { MetricCard } from '../components/MetricCard';
import { StatusBadge } from '../components/StatusBadge';

interface ModelOverviewViewProps {
  model?: ModelDetail;
  analysis?: AnalysisResponse;
  onRunXRay: () => void;
  onGoToAutopilot: () => void;
  onGoToSolve: () => void;
  isAnalyzing?: boolean;
}

export const ModelOverviewView: React.FC<ModelOverviewViewProps> = ({
  model,
  analysis,
  onRunXRay,
  onGoToSolve,
  isAnalyzing = false
}) => {
  if (!model) {
    return (
      <div className="p-8 text-center text-slate-500">
        No model selected. Import a model or choose a synthetic benchmark.
      </div>
    );
  }

  const profile = analysis?.profile;

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      {/* Header Banner */}
      <div className="bg-[#121824] border border-[#232e42] rounded-xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <h1 className="text-xl font-bold tracking-tight text-slate-100">{model.display_name}</h1>
            <StatusBadge status={model.dataset_kind} size="sm" />
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
              {model.current_version?.format.toUpperCase() || 'MPS'}
            </span>
          </div>
          <p className="text-xs text-slate-400 font-mono flex items-center gap-2">
            <span>Model ID: {model.model_id}</span>
            <span>•</span>
            <span>SHA256: {model.current_version?.sha256.slice(0, 16)}...</span>
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onRunXRay}
            disabled={isAnalyzing}
            className="flex items-center gap-2 px-3.5 py-2 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold tracking-wider transition-colors border border-slate-700 cursor-pointer disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isAnalyzing ? 'animate-spin text-sky-400' : ''}`} />
            {isAnalyzing ? 'Analyzing...' : 'Run Model X-Ray'}
          </button>
          <button
            onClick={onGoToSolve}
            className="flex items-center gap-2 px-4 py-2 rounded bg-sky-600 hover:bg-sky-500 text-slate-950 text-xs font-semibold tracking-wider transition-colors shadow-sm cursor-pointer"
          >
            <Zap className="w-3.5 h-3.5 fill-current" />
            Solve Model
          </button>
        </div>
      </div>

      {/* Primary Mathematical Profile Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard
          label="Decision Variables"
          value={profile ? profile.variables : '—'}
          unit="cols"
          subtext={profile ? `${(profile.integer_ratio * 100).toFixed(0)}% integer variables` : 'Pending analysis'}
        />
        <MetricCard
          label="Linear Constraints"
          value={profile ? profile.constraints : '—'}
          unit="rows"
          subtext={profile ? `${profile.singleton_rows} singleton bounds` : 'Pending analysis'}
        />
        <MetricCard
          label="Nonzero Elements"
          value={profile ? profile.nonzeros : '—'}
          unit="entries"
          subtext={profile ? `Density: ${(profile.density * 100).toFixed(4)}%` : 'Pending analysis'}
          highlight
        />
        <MetricCard
          label="Formulation Risk"
          value={analysis?.risk.level || 'UNANALYZED'}
          badge={analysis ? <StatusBadge status={analysis.risk.level} size="sm" /> : undefined}
          subtext={analysis ? `${analysis.risk.issues.length} detected condition issues` : 'Run X-Ray to diagnose'}
        />
      </div>

      {/* Architecture & Verification Confidence Box */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-[#121824] border border-[#232e42] rounded-lg p-5">
          <h3 className="text-sm font-semibold text-slate-200 mb-3 flex items-center gap-2">
            <Layers className="w-4 h-4 text-sky-400" />
            Sovereignty & Numerical Path
          </h3>
          <ul className="space-y-2 text-xs text-slate-400 leading-relaxed">
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>Clean-room implementation: zero external commercial solver dependencies inside runtime.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>Deterministic Autopilot rules select CPU/CUDA acceleration based on nonzero structure.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>High-performance Ruiz equilibration & continuous PDHG solver kernel.</span>
            </li>
          </ul>
        </div>

        <div className="bg-[#121824] border border-[#232e42] rounded-lg p-5">
          <h3 className="text-sm font-semibold text-slate-200 mb-3 flex items-center gap-2">
            <Shield className="w-4 h-4 text-emerald-400" />
            Independent Decision Verification
          </h3>
          <p className="text-xs text-slate-400 mb-3 leading-relaxed">
            Every solution returned by NIYAM-X is paired with an independent Proof Pack that verifies bounds,
            constraint satisfaction, and objective reconstruction without touching the optimizer.
          </p>
          <div className="flex items-center gap-3 pt-2 border-t border-[#232e42] text-xs">
            <span className="text-slate-400 font-mono">Verifier binary:</span>
            <span className="text-emerald-400 font-mono font-semibold">niyam-verify (stand-alone)</span>
          </div>
        </div>
      </div>
    </div>
  );
};
