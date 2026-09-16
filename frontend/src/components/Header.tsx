import React from 'react';
import { ShieldCheck, Cpu, Zap, Layers } from 'lucide-react';
import type { ModelSummary, HardwareResponse, HealthResponse } from '../api/types';

interface HeaderProps {
  models: ModelSummary[];
  selectedModelId: string;
  onSelectModel: (id: string) => void;
  hardware?: HardwareResponse;
  health?: HealthResponse;
  onQuickSolve?: () => void;
  isSolving?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  models,
  selectedModelId,
  onSelectModel,
  hardware,
  health,
  onQuickSolve,
  isSolving = false
}) => {
  const currentModel = models.find((m) => m.model_id === selectedModelId);

  return (
    <header className="h-16 border-b border-[#232e42] bg-[#0b0e14] px-6 flex items-center justify-between sticky top-0 z-30">
      {/* Brand & Tagline */}
      <div className="flex items-center gap-5">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded bg-gradient-to-br from-sky-500 to-sky-700 flex items-center justify-center text-slate-950 font-black tracking-widest text-base shadow-sm">
            N
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold tracking-wider text-slate-100 text-lg">NIYAM-X</span>
              <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-sky-950/80 text-sky-400 border border-sky-800/60">
                Sovereign Core
              </span>
            </div>
            <div className="text-[11px] text-slate-400 tracking-wider uppercase font-medium">
              Solve. Adapt. Prove.
            </div>
          </div>
        </div>

        {/* Model Selector Pill */}
        <div className="hidden md:flex items-center gap-2 pl-4 border-l border-[#232e42]">
          <Layers className="w-4 h-4 text-slate-400" />
          <select
            value={selectedModelId}
            onChange={(e) => onSelectModel(e.target.value)}
            className="bg-[#121824] border border-[#232e42] text-slate-200 text-xs rounded px-3 py-1.5 focus:outline-none focus:border-sky-500 font-medium"
          >
            {models.map((m) => (
              <option key={m.model_id} value={m.model_id}>
                {m.display_name} ({m.dataset_kind})
              </option>
            ))}
          </select>
          {currentModel && (
            <span className="text-[11px] font-mono text-slate-400">
              {currentModel.model_id.slice(0, 10)}
            </span>
          )}
        </div>
      </div>

      {/* Right Controls: Hardware, Verification, Action */}
      <div className="flex items-center gap-4">
        {/* GPU / Hardware Indicator */}
        <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded bg-[#121824] border border-[#232e42] text-xs">
          <Cpu className="w-3.5 h-3.5 text-sky-400" />
          <span className="text-slate-400 font-medium">Engine:</span>
          {hardware?.gpu.cuda_available ? (
            <span className="font-mono text-cyan-400 font-medium flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping" />
              {hardware.gpu.name.replace("NVIDIA GeForce ", "")} (CUDA)
            </span>
          ) : (
            <span className="font-mono text-slate-300">CPU Sovereign</span>
          )}
        </div>

        {/* Verifier Badge */}
        <div className="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded bg-[#121824] border border-[#232e42] text-xs">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-slate-400 font-medium">Verifier:</span>
          <span className="text-emerald-400 font-mono">
            {health?.verifier_available ? 'Independent Online' : 'Active'}
          </span>
        </div>

        {/* Quick Solve Action */}
        {onQuickSolve && (
          <button
            onClick={onQuickSolve}
            disabled={isSolving}
            className="flex items-center gap-2 px-4 py-1.5 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-800 disabled:text-slate-600 text-slate-950 font-semibold text-xs tracking-wider rounded transition-all shadow-sm active:scale-95 cursor-pointer disabled:cursor-not-allowed"
          >
            <Zap className="w-3.5 h-3.5 fill-current" />
            {isSolving ? 'Solving...' : 'Execute Solve'}
          </button>
        )}
      </div>
    </header>
  );
};
