import React from 'react';
import { clsx } from 'clsx';

interface StatusBadgeProps {
  status: string;
  className?: string;
  size?: 'sm' | 'md';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, className, size = 'md' }) => {
  const normalized = status.toUpperCase();

  let colorClasses = 'bg-slate-800 text-slate-300 border-slate-700';

  if (normalized === 'OPTIMAL' || normalized === 'VERIFIED') {
    colorClasses = 'bg-emerald-950/70 text-emerald-400 border-emerald-800/80';
  } else if (normalized === 'RUNNING' || normalized === 'STARTING') {
    colorClasses = 'bg-sky-950/70 text-sky-400 border-sky-800/80 animate-pulse';
  } else if (normalized === 'QUEUED') {
    colorClasses = 'bg-indigo-950/70 text-indigo-300 border-indigo-800/80';
  } else if (normalized === 'FEASIBLE' || normalized === 'TIME LIMIT' || normalized === 'MEDIUM') {
    colorClasses = 'bg-amber-950/70 text-amber-400 border-amber-800/80';
  } else if (normalized === 'HIGH' || normalized === 'FAILED' || normalized === 'VERIFICATION_FAILED' || normalized === 'NUMERICAL_FAILURE') {
    colorClasses = 'bg-rose-950/70 text-rose-400 border-rose-800/80';
  } else if (normalized === 'LOW') {
    colorClasses = 'bg-slate-900 text-emerald-400 border-slate-700';
  } else if (normalized === 'CUDA' || normalized === 'ROBUST') {
    colorClasses = 'bg-cyan-950/70 text-cyan-300 border-cyan-800/80';
  } else if (normalized === 'CPU' || normalized === 'BASIC') {
    colorClasses = 'bg-slate-900 text-slate-300 border-slate-700';
  }

  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-[11px]' : 'px-2.5 py-1 text-xs';

  return (
    <span
      className={clsx(
        'inline-flex items-center gap-1.5 rounded font-mono font-medium tracking-wide uppercase border',
        sizeClasses,
        colorClasses,
        className
      )}
    >
      <span className="w-1.5 h-1.5 rounded-full bg-current opacity-80" />
      {normalized}
    </span>
  );
};
