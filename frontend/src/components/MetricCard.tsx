import React from 'react';
import { clsx } from 'clsx';

interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  subtext?: string;
  badge?: React.ReactNode;
  highlight?: boolean;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  unit,
  subtext,
  badge,
  highlight = false,
  className
}) => {
  return (
    <div
      className={clsx(
        'rounded-lg p-4 border transition-colors',
        highlight
          ? 'bg-slate-900/90 border-sky-500/40 shadow-sm shadow-sky-950/20'
          : 'bg-[#121824] border-[#232e42] hover:border-slate-700',
        className
      )}
    >
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{label}</span>
        {badge}
      </div>
      <div className="flex items-baseline gap-1.5">
        <span className="text-2xl font-semibold font-mono tracking-tight text-slate-100">
          {typeof value === 'number' && !Number.isInteger(value)
            ? value < 0.001 && value > 0
              ? value.toExponential(2)
              : value.toLocaleString(undefined, { maximumFractionDigits: 3 })
            : value}
        </span>
        {unit && <span className="text-xs text-slate-400 font-mono">{unit}</span>}
      </div>
      {subtext && <div className="mt-1 text-xs text-slate-500">{subtext}</div>}
    </div>
  );
};
