import React from 'react';
import {
  Activity,
  Sliders,
  Play,
  GitCompare,
  ShieldCheck,
  BarChart2,
  FileText
} from 'lucide-react';
import { clsx } from 'clsx';

export type TabKey = 'overview' | 'xray' | 'autopilot' | 'solve' | 'delta' | 'proof' | 'benchmarks';

interface SidebarProps {
  activeTab: TabKey;
  onTabChange: (tab: TabKey) => void;
  solveStatus?: string;
  hasVerification?: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  onTabChange,
  solveStatus,
  hasVerification = false
}) => {
  const navItems: { key: TabKey; label: string; icon: React.ComponentType<{ className?: string }>; tag?: string }[] = [
    { key: 'overview', label: 'Model Overview', icon: FileText },
    { key: 'xray', label: 'Model X-Ray', icon: Activity, tag: 'Analysis' },
    { key: 'autopilot', label: 'Solver Autopilot', icon: Sliders, tag: 'Plan' },
    { key: 'solve', label: 'Live Telemetry', icon: Play, tag: solveStatus || 'Ready' },
    { key: 'delta', label: 'DeltaSolve What-If', icon: GitCompare, tag: 'Re-Solve' },
    { key: 'proof', label: 'Proof Pack', icon: ShieldCheck, tag: hasVerification ? 'Verified' : 'Audit' },
    { key: 'benchmarks', label: 'Benchmarks', icon: BarChart2, tag: 'CPU/GPU' }
  ];

  return (
    <aside className="w-64 border-r border-[#232e42] bg-[#0d121b] flex flex-col justify-between select-none">
      <div className="p-3">
        <div className="px-3 py-2 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
          Workbench Workspace
        </div>
        <nav className="space-y-1 mt-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.key;
            return (
              <button
                key={item.key}
                onClick={() => onTabChange(item.key)}
                className={clsx(
                  'w-full flex items-center justify-between px-3 py-2 rounded text-xs font-medium transition-colors text-left cursor-pointer',
                  isActive
                    ? 'bg-sky-950/60 text-sky-400 border border-sky-800/60 shadow-inner'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-[#121824]'
                )}
              >
                <div className="flex items-center gap-2.5">
                  <Icon className={clsx('w-4 h-4', isActive ? 'text-sky-400' : 'text-slate-400')} />
                  <span>{item.label}</span>
                </div>
                {item.tag && (
                  <span
                    className={clsx(
                      'text-[10px] font-mono px-1.5 py-0.2 rounded uppercase',
                      isActive ? 'bg-sky-900/60 text-sky-300' : 'bg-slate-800/80 text-slate-400'
                    )}
                  >
                    {item.tag}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Clean-Room Protocol Notice */}
      <div className="p-4 border-t border-[#232e42] bg-[#0b0e14]/50 text-[11px] text-slate-400 leading-relaxed">
        <div className="font-semibold text-slate-300 mb-1 flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
          Clean-Room Sovereign
        </div>
        Zero commercial solver calls. Solver mathematics & control paths are proprietary NIYAM-X kernels.
      </div>
    </aside>
  );
};
