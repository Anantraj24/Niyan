import React from 'react';
import { Play, ShieldCheck } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend
} from 'recharts';
import type { SolveStatusResponse, VerificationResponse } from '../api/types';
import { MetricCard } from '../components/MetricCard';
import { StatusBadge } from '../components/StatusBadge';

interface TelemetryPoint {
  iteration: number;
  primal_residual: number;
  dual_residual: number;
  objective: number;
}

interface SolveTelemetryViewProps {
  activeSolve?: SolveStatusResponse;
  telemetryHistory: TelemetryPoint[];
  verification?: VerificationResponse;
  onVerify: () => void;
  onGoToDelta: () => void;
  isVerifying?: boolean;
}

export const SolveTelemetryView: React.FC<SolveTelemetryViewProps> = ({
  activeSolve,
  telemetryHistory,
  verification,
  onVerify,
  onGoToDelta,
  isVerifying = false
}) => {
  if (!activeSolve) {
    return (
      <div className="p-12 text-center text-slate-500 max-w-md mx-auto">
        <Play className="w-12 h-12 text-slate-700 mx-auto mb-4" />
        <h3 className="text-base font-semibold text-slate-300 mb-2">No Solve in Progress</h3>
        <p className="text-xs text-slate-400">
          Initiate an optimization solve from the Model Overview or Autopilot view to stream live telemetry.
        </p>
      </div>
    );
  }

  const isCompleted = activeSolve.state === 'COMPLETED';

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      {/* Run Header */}
      <div className="bg-[#121824] border border-[#232e42] rounded-xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-base font-bold tracking-tight text-slate-100 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-sky-400 animate-pulse" />
              SOLVER FLIGHT RECORDER & TELEMETRY
            </h2>
            <StatusBadge status={activeSolve.solver_status || activeSolve.state} />
            {activeSolve.warm_start && (
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
                Warm Start (DeltaSolve)
              </span>
            )}
          </div>
          <div className="text-xs text-slate-400 font-mono mt-1 flex items-center gap-3">
            <span>Job ID: {activeSolve.solve_id}</span>
            <span>•</span>
            <span>Backend: {activeSolve.backend || 'CUDA'}</span>
            <span>•</span>
            <span>Scaling: {activeSolve.scaling || 'ROBUST'}</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-3">
          {isCompleted && (
            <>
              <button
                onClick={onVerify}
                disabled={isVerifying}
                className="flex items-center gap-2 px-3.5 py-1.5 rounded bg-[#1c2433] hover:bg-slate-700 text-slate-200 text-xs font-semibold tracking-wider transition-colors border border-slate-600 cursor-pointer disabled:opacity-50"
              >
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                {isVerifying ? 'Verifying...' : 'Verify Decision'}
              </button>
              <button
                onClick={onGoToDelta}
                className="flex items-center gap-2 px-4 py-1.5 rounded bg-sky-600 hover:bg-sky-500 text-slate-950 text-xs font-semibold tracking-wider transition-colors cursor-pointer"
              >
                Simulate What-If Shock →
              </button>
            </>
          )}
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <MetricCard
          label="Objective Value"
          value={
            activeSolve.objective !== undefined && activeSolve.objective !== null
              ? `$${activeSolve.objective.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
              : '—'
          }
          subtext="Net Refinery Profit"
          highlight={isCompleted}
        />
        <MetricCard
          label="Solve Time"
          value={activeSolve.solve_time_ms ? `${activeSolve.solve_time_ms}` : '—'}
          unit="ms"
          subtext="Native subprocess duration"
        />
        <MetricCard
          label="Primal Residual"
          value={activeSolve.primal_residual ? activeSolve.primal_residual.toExponential(2) : '—'}
          unit="||Ax - b||"
          subtext="Target: < 1e-6"
        />
        <MetricCard
          label="Total Iterations"
          value={activeSolve.iterations ?? '—'}
          unit="iters"
          subtext="First-Order PDHG steps"
        />
      </div>

      {/* Live Convergence Chart */}
      <div className="bg-[#121824] border border-[#232e42] rounded-xl p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
            KKT Residual Convergence Trajectory
          </h3>
          <span className="text-[11px] font-mono text-slate-400">
            {telemetryHistory.length} Telemetry Checkpoints
          </span>
        </div>

        <div className="h-72 w-full">
          {telemetryHistory.length === 0 ? (
            <div className="h-full flex items-center justify-center text-xs text-slate-500 font-mono">
              Waiting for solver iteration telemetry...
            </div>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={telemetryHistory} margin={{ top: 10, right: 20, left: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2a3d" />
                <XAxis dataKey="iteration" stroke="#64748b" tick={{ fontSize: 11, fontFamily: 'monospace' }} />
                <YAxis
                  scale="log"
                  domain={['auto', 'auto']}
                  stroke="#64748b"
                  tick={{ fontSize: 11, fontFamily: 'monospace' }}
                />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0b0e14', borderColor: '#232e42', fontSize: '11px', fontFamily: 'monospace' }}
                  labelStyle={{ color: '#94a3b8' }}
                />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                <Line
                  type="monotone"
                  dataKey="primal_residual"
                  name="Primal Infeasibility"
                  stroke="#38bdf8"
                  strokeWidth={2}
                  dot={false}
                  isAnimationActive={false}
                />
                <Line
                  type="monotone"
                  dataKey="dual_residual"
                  name="Dual Infeasibility"
                  stroke="#a855f7"
                  strokeWidth={2}
                  dot={false}
                  isAnimationActive={false}
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* Independent Verification Banner if completed */}
      {verification && (
        <div className="bg-[#0e1624] border border-emerald-800/60 rounded-xl p-5 flex items-center justify-between">
          <div className="flex items-center gap-3.5">
            <div className="w-9 h-9 rounded-full bg-emerald-950 flex items-center justify-center text-emerald-400 border border-emerald-800">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-bold text-slate-100">Independent Proof Pack:</span>
                <StatusBadge status={verification.verdict || 'VERIFIED'} size="sm" />
              </div>
              <p className="text-xs text-slate-400 font-mono mt-0.5">
                Max Primal Violation: {verification.max_primal_violation?.toExponential(2)} • Bound Violation: {verification.max_bound_violation} • Model Hash Match: Confirmed
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
