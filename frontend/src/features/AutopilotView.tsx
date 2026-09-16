import React, { useState } from 'react';
import { Sliders, Zap, CheckCircle2, ArrowRight } from 'lucide-react';
import type { AnalysisResponse, SolveConfig } from '../api/types';
import { StatusBadge } from '../components/StatusBadge';

interface AutopilotViewProps {
  analysis?: AnalysisResponse;
  onExecuteSolve: (config: SolveConfig) => void;
  isSolving?: boolean;
}

export const AutopilotView: React.FC<AutopilotViewProps> = ({
  analysis,
  onExecuteSolve,
  isSolving = false
}) => {
  const [backend, setBackend] = useState<string>(analysis?.autopilot.backend || 'AUTO');
  const [scaling, setScaling] = useState<string>(analysis?.autopilot.scaling || 'AUTO');
  const [timeLimit, setTimeLimit] = useState<number>(30);
  const [tolerance, setTolerance] = useState<number>(1e-6);

  const handleSolve = () => {
    onExecuteSolve({
      backend,
      scaling,
      time_limit_sec: timeLimit,
      tolerance
    });
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      {/* Title */}
      <div>
        <div className="flex items-center gap-2">
          <Sliders className="w-5 h-5 text-sky-400" />
          <h2 className="text-lg font-bold tracking-tight text-slate-100">SOLVER AUTOPILOT</h2>
        </div>
        <p className="text-xs text-slate-400 mt-1">
          Deterministic execution planning: chooses backend hardware, matrix scaling, and convergence tolerances.
        </p>
      </div>

      {/* Autopilot Strategy Plan Card */}
      <div className="bg-[#121824] border border-[#232e42] rounded-xl p-6 space-y-6">
        <div className="flex items-center justify-between border-b border-[#232e42] pb-4">
          <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Autonomous Strategy Selection
          </span>
          <StatusBadge status={backend} />
        </div>

        {/* Selected Strategy Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-lg bg-[#0e141f] border border-[#1f2a3d]">
            <div className="text-[11px] font-semibold text-slate-400 uppercase mb-1">Target Backend</div>
            <div className="text-base font-mono font-bold text-slate-100 mb-2">
              {backend === 'AUTO' ? analysis?.autopilot.backend || 'CUDA' : backend}
            </div>
            <p className="text-[11px] text-slate-400 leading-normal">
              {backend === 'CUDA' || (backend === 'AUTO' && analysis?.autopilot.backend === 'CUDA')
                ? 'High-throughput parallel sparse matrix kernel on GPU.'
                : 'Deterministic single-process reference solver on CPU.'}
            </p>
          </div>

          <div className="p-4 rounded-lg bg-[#0e141f] border border-[#1f2a3d]">
            <div className="text-[11px] font-semibold text-slate-400 uppercase mb-1">Scaling Mode</div>
            <div className="text-base font-mono font-bold text-slate-100 mb-2">
              {scaling === 'AUTO' ? analysis?.autopilot.scaling || 'ROBUST' : scaling}
            </div>
            <p className="text-[11px] text-slate-400 leading-normal">
              Ruiz equilibration to compress dynamic coefficient ranges.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-[#0e141f] border border-[#1f2a3d]">
            <div className="text-[11px] font-semibold text-slate-400 uppercase mb-1">Warm Re-optimization</div>
            <div className="text-base font-mono font-bold text-emerald-400 mb-2">
              ELIGIBLE (DeltaSolve)
            </div>
            <p className="text-[11px] text-slate-400 leading-normal">
              Fast parameter shock re-solves via state vector reuse.
            </p>
          </div>
        </div>

        {/* Autopilot Rationale */}
        {analysis?.autopilot.reasons && (
          <div className="p-4 rounded-lg bg-[#0b0e14] border border-[#1c2638] text-xs">
            <span className="text-[11px] font-semibold uppercase text-slate-400 block mb-2">
              Mathematical Rationale
            </span>
            <ul className="space-y-1.5 text-slate-300">
              {analysis.autopilot.reasons.map((reason, i) => (
                <li key={i} className="flex items-start gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-sky-400 shrink-0 mt-0.5" />
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Runtime Adjustments Form */}
        <div className="pt-4 border-t border-[#232e42] grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="block text-slate-300 font-medium mb-1.5">Execution Backend Override</label>
            <select
              value={backend}
              onChange={(e) => setBackend(e.target.value)}
              className="w-full bg-[#0b0e14] border border-[#232e42] rounded px-3 py-2 text-slate-200 font-mono text-xs focus:outline-none focus:border-sky-500"
            >
              <option value="AUTO">AUTO (Let Autopilot Select)</option>
              <option value="CUDA">CUDA (NVIDIA Accelerated)</option>
              <option value="CPU">CPU (Clean-Room Host)</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1.5">Equilibration Scaling</label>
            <select
              value={scaling}
              onChange={(e) => setScaling(e.target.value)}
              className="w-full bg-[#0b0e14] border border-[#232e42] rounded px-3 py-2 text-slate-200 font-mono text-xs focus:outline-none focus:border-sky-500"
            >
              <option value="AUTO">AUTO (Heuristic Selection)</option>
              <option value="ROBUST">ROBUST (Ruiz Equilibration)</option>
              <option value="BASIC">BASIC (Geometric Mean)</option>
              <option value="NONE">NONE (Raw Input Matrix)</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1.5">Time Limit (Seconds)</label>
            <input
              type="number"
              value={timeLimit}
              onChange={(e) => setTimeLimit(Number(e.target.value))}
              min={1}
              max={300}
              className="w-full bg-[#0b0e14] border border-[#232e42] rounded px-3 py-2 text-slate-200 font-mono text-xs focus:outline-none focus:border-sky-500"
            />
          </div>

          <div>
            <label className="block text-slate-300 font-medium mb-1.5">Convergence Tolerance ($\epsilon$)</label>
            <select
              value={tolerance}
              onChange={(e) => setTolerance(Number(e.target.value))}
              className="w-full bg-[#0b0e14] border border-[#232e42] rounded px-3 py-2 text-slate-200 font-mono text-xs focus:outline-none focus:border-sky-500"
            >
              <option value={1e-4}>1e-4 (Fast Coarse)</option>
              <option value={1e-6}>1e-6 (Industrial Standard)</option>
              <option value={1e-8}>1e-8 (High Precision)</option>
            </select>
          </div>
        </div>

        {/* Action Button */}
        <div className="pt-2 flex justify-end">
          <button
            onClick={handleSolve}
            disabled={isSolving}
            className="flex items-center gap-2 px-6 py-2.5 rounded bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-slate-950 text-xs font-bold uppercase tracking-wider transition-all shadow cursor-pointer"
          >
            <Zap className="w-4 h-4 fill-current" />
            {isSolving ? 'Solving in Progress...' : 'Launch Solve With This Plan'}
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
