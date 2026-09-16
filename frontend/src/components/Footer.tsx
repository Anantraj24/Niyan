import React from 'react';
import { ShieldCheck, Cpu, Terminal, Radio } from 'lucide-react';
import type { HealthResponse, HardwareResponse, SolveStatusResponse } from '../api/types';

interface FooterProps {
  health?: HealthResponse;
  hardware?: HardwareResponse;
  activeSolve?: SolveStatusResponse;
}

export const Footer: React.FC<FooterProps> = ({ health, hardware, activeSolve }) => {
  return (
    <footer className="h-8 border-t border-[#232e42] bg-[#0b0e14] px-4 flex items-center justify-between text-[11px] text-slate-400 font-mono select-none">
      <div className="flex items-center gap-5">
        <div className="flex items-center gap-1.5">
          <Radio className="w-3 h-3 text-emerald-400 animate-pulse" />
          <span>API: {health?.status === 'ok' ? 'Connected' : 'Connecting'}</span>
        </div>

        <div className="hidden sm:flex items-center gap-1.5 border-l border-[#232e42] pl-4">
          <Terminal className="w-3 h-3 text-sky-400" />
          <span>Kernel: v0.1.0-cleanroom</span>
        </div>

        <div className="hidden md:flex items-center gap-1.5 border-l border-[#232e42] pl-4">
          <Cpu className="w-3 h-3 text-slate-400" />
          <span>
            {hardware?.gpu.cuda_available
              ? `${hardware.gpu.name.replace("NVIDIA GeForce ", "")} [CUDA Active]`
              : `${hardware?.cpu.name || 'CPU Host'} [Single-Process]`}
          </span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {activeSolve ? (
          <div className="flex items-center gap-2">
            <span className="text-slate-400">Run:</span>
            <span className="text-slate-300 font-semibold">{activeSolve.solve_id}</span>
            <span className="text-sky-400 uppercase">[{activeSolve.state}]</span>
          </div>
        ) : (
          <span className="text-slate-400">Idle / Ready</span>
        )}

        <div className="flex items-center gap-1.5 border-l border-[#232e42] pl-3 text-emerald-400">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Audit Active</span>
        </div>
      </div>
    </footer>
  );
};
