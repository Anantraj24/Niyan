import React from 'react';
import { Activity, CheckCircle, ShieldAlert, Cpu } from 'lucide-react';
import type { AnalysisResponse } from '../api/types';
import { MetricCard } from '../components/MetricCard';
import { StatusBadge } from '../components/StatusBadge';

interface ModelXRayViewProps {
  analysis?: AnalysisResponse;
  onRunXRay: () => void;
  onGoToAutopilot: () => void;
  isAnalyzing?: boolean;
}

export const ModelXRayView: React.FC<ModelXRayViewProps> = ({
  analysis,
  onRunXRay,
  onGoToAutopilot,
  isAnalyzing = false
}) => {
  if (!analysis) {
    return (
      <div className="p-12 text-center max-w-lg mx-auto">
        <Activity className="w-12 h-12 text-slate-600 mx-auto mb-4" />
        <h3 className="text-base font-semibold text-slate-200 mb-2">Model Not Yet Analyzed</h3>
        <p className="text-xs text-slate-400 mb-6 leading-relaxed">
          Run Model X-Ray to inspect sparsity, matrix conditioning, dynamic range, and formulation risk heuristics.
        </p>
        <button
          onClick={onRunXRay}
          disabled={isAnalyzing}
          className="px-5 py-2.5 rounded bg-sky-600 hover:bg-sky-500 text-slate-950 text-xs font-semibold uppercase tracking-wider transition-colors cursor-pointer disabled:opacity-50"
        >
          {isAnalyzing ? 'Analyzing Structure...' : 'Execute Model X-Ray'}
        </button>
      </div>
    );
  }

  const { profile, risk, autopilot } = analysis;

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      {/* Top Title & Quick Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-lg font-bold tracking-tight text-slate-100 flex items-center gap-2">
              <Activity className="w-5 h-5 text-sky-400" />
              MODEL X-RAY DIAGNOSTICS
            </h2>
            <StatusBadge status={risk.level} />
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Structural decomposition and numerical conditioning inspection for sovereign solve planning.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onRunXRay}
            disabled={isAnalyzing}
            className="px-3.5 py-1.5 rounded bg-[#121824] hover:bg-slate-800 text-slate-300 text-xs font-medium border border-[#232e42] transition-colors cursor-pointer"
          >
            {isAnalyzing ? 'Refreshing...' : 'Re-Run Inspection'}
          </button>
          <button
            onClick={onGoToAutopilot}
            className="px-4 py-1.5 rounded bg-sky-600 hover:bg-sky-500 text-slate-950 text-xs font-semibold tracking-wider transition-colors cursor-pointer"
          >
            Inspect Autopilot Plan →
          </button>
        </div>
      </div>

      {/* Numerical Inspection Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <MetricCard
          label="Risk Profile"
          value={risk.level}
          badge={<StatusBadge status={risk.level} size="sm" />}
        />
        <MetricCard
          label="Matrix Sparsity"
          value={`${((1 - profile.density) * 100).toFixed(2)}%`}
          subtext={`${profile.nonzeros} nonzeros`}
        />
        <MetricCard
          label="Dynamic Range"
          value={profile.coefficient_dynamic_range.toExponential(1)}
          subtext="max |a| / min |a|"
          highlight={profile.coefficient_dynamic_range > 1e4}
        />
        <MetricCard
          label="Min Nonzero |a|"
          value={profile.coefficient_min_abs.toExponential(2)}
          subtext="Smallest magnitude"
        />
        <MetricCard
          label="Max Nonzero |a|"
          value={profile.coefficient_max_abs.toLocaleString()}
          subtext="Largest magnitude"
        />
        <MetricCard
          label="Fixed Variables"
          value={profile.fixed_variables}
          subtext="Presovable bound"
        />
      </div>

      {/* Two Column Layout: Identified Conditioning Issues & Autopilot Strategic Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Identified Issues */}
        <div className="bg-[#121824] border border-[#232e42] rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-amber-400" />
              Identified Numerical & Formulation Issues
            </h3>
            <span className="text-xs font-mono text-slate-400">
              {risk.issues.length} {risk.issues.length === 1 ? 'Condition' : 'Conditions'} Flagged
            </span>
          </div>

          {risk.issues.length === 0 ? (
            <div className="p-4 rounded-lg bg-emerald-950/20 border border-emerald-800/40 text-xs text-emerald-300 flex items-center gap-2.5">
              <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>Well-conditioned matrix formulation. No severe numerical scaling risks detected.</span>
            </div>
          ) : (
            <div className="space-y-2.5">
              {risk.issues.map((issue, idx) => (
                <div
                  key={idx}
                  className="p-3.5 rounded-lg bg-[#0e141f] border border-[#1f2a3d] flex items-start justify-between gap-3 text-xs"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-slate-200 font-medium">{issue.code}</span>
                      <StatusBadge status={issue.severity} size="sm" />
                    </div>
                    <p className="text-slate-400 leading-relaxed">{issue.message}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Strategic Recommendations */}
        <div className="bg-[#121824] border border-[#232e42] rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-cyan-400" />
              Autopilot Formulation Strategy
            </h3>
            <span className="text-xs font-mono text-cyan-400 uppercase tracking-wide font-medium">
              Deterministic Rules
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-lg bg-[#0e141f] border border-[#1f2a3d] flex items-center justify-between">
              <div>
                <div className="text-[11px] text-slate-400 uppercase font-semibold">Recommended Backend</div>
                <div className="text-sm font-mono font-bold text-slate-100">{autopilot.backend}</div>
              </div>
              <StatusBadge status={autopilot.backend} />
            </div>

            <div className="p-3 rounded-lg bg-[#0e141f] border border-[#1f2a3d] flex items-center justify-between">
              <div>
                <div className="text-[11px] text-slate-400 uppercase font-semibold">Equilibration Scaling</div>
                <div className="text-sm font-mono font-bold text-slate-100">{autopilot.scaling}</div>
              </div>
              <StatusBadge status={autopilot.scaling} />
            </div>

            <div className="p-3.5 rounded-lg bg-[#0e141f] border border-[#1f2a3d]">
              <div className="text-[11px] text-slate-400 uppercase font-semibold mb-2">Technical Rationale</div>
              <ul className="space-y-1.5 text-slate-300 list-disc list-inside">
                {autopilot.reasons.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
