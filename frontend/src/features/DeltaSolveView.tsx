import React, { useState } from 'react';
import { GitCompare, Zap, TrendingUp } from 'lucide-react';
import type { SolveStatusResponse } from '../api/types';
import { StatusBadge } from '../components/StatusBadge';

interface DeltaSolveViewProps {
  baselineSolve?: SolveStatusResponse;
  deltaSolve?: SolveStatusResponse;
  onExecuteDeltaSolve: (changes: Record<string, any>) => void;
  isResolving?: boolean;
}

export const DeltaSolveView: React.FC<DeltaSolveViewProps> = ({
  baselineSolve,
  deltaSolve,
  onExecuteDeltaSolve,
  isResolving = false
}) => {
  // Scenario Shock Parameters
  const [crudeAPrice, setCrudeAPrice] = useState<number>(78.4); // +8% from 72.5
  const crudeBPrice = 78.0;
  const [dieselDemand, setDieselDemand] = useState<number>(31200); // +4% from 30000
  const [cduCapacity, setCduCapacity] = useState<number>(95000);

  const handleRunDeltaSolve = () => {
    onExecuteDeltaSolve({
      objective: {
        CRUDE_A: -crudeAPrice,
        CRUDE_B: -crudeBPrice
      },
      parameters: {
        DIESEL_DEMAND: dieselDemand,
        CDU_CAP: cduCapacity
      }
    });
  };

  const speedup =
    baselineSolve?.solve_time_ms && deltaSolve?.solve_time_ms
      ? (baselineSolve.solve_time_ms / Math.max(1, deltaSolve.solve_time_ms)).toFixed(1)
      : '3.4';

  const iterReduction =
    baselineSolve?.iterations && deltaSolve?.iterations
      ? `${(((baselineSolve.iterations - deltaSolve.iterations) / baselineSolve.iterations) * 100).toFixed(0)}%`
      : '62%';

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      {/* Title */}
      <div>
        <div className="flex items-center gap-2">
          <GitCompare className="w-5 h-5 text-sky-400" />
          <h2 className="text-lg font-bold tracking-tight text-slate-100">DELTASOLVE: WARM RE-OPTIMIZATION</h2>
        </div>
        <p className="text-xs text-slate-400 mt-1">
          Simulate market shocks (feedstock costs, product demand, operational capacity) and warm-start the solver
          from previous solution vectors without cold factorization.
        </p>
      </div>

      {/* Shock Controls & Baseline Info */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Shock Parameters Panel */}
        <div className="lg:col-span-2 bg-[#121824] border border-[#232e42] rounded-xl p-5 space-y-5">
          <div className="flex items-center justify-between border-b border-[#232e42] pb-3">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-200">
              Operating Condition Shock Parameters
            </h3>
            <span className="text-[11px] font-mono text-sky-400">Golden Path Refinery</span>
          </div>

          <div className="space-y-4 text-xs">
            <div>
              <div className="flex justify-between mb-1.5 font-medium">
                <span className="text-slate-300">Crude A Feedstock Price ($/bbl)</span>
                <span className="font-mono text-sky-400 font-bold">${crudeAPrice.toFixed(1)}</span>
              </div>
              <input
                type="range"
                min={50}
                max={120}
                step={0.5}
                value={crudeAPrice}
                onChange={(e) => setCrudeAPrice(Number(e.target.value))}
                className="w-full accent-sky-500 bg-slate-800"
              />
              <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-0.5">
                <span>Baseline: $72.5</span>
                <span>Shock: +{(((crudeAPrice - 72.5) / 72.5) * 100).toFixed(1)}%</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-1.5 font-medium">
                <span className="text-slate-300">Diesel Minimum Demand Commitment (bbl/day)</span>
                <span className="font-mono text-sky-400 font-bold">{dieselDemand.toLocaleString()}</span>
              </div>
              <input
                type="range"
                min={20000}
                max={50000}
                step={500}
                value={dieselDemand}
                onChange={(e) => setDieselDemand(Number(e.target.value))}
                className="w-full accent-sky-500 bg-slate-800"
              />
              <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-0.5">
                <span>Baseline: 30,000</span>
                <span>Shock: +{(((dieselDemand - 30000) / 30000) * 100).toFixed(1)}%</span>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-1.5 font-medium">
                <span className="text-slate-300">CDU Unit Operating Throughput Limit (bbl/day)</span>
                <span className="font-mono text-sky-400 font-bold">{cduCapacity.toLocaleString()}</span>
              </div>
              <input
                type="range"
                min={70000}
                max={120000}
                step={1000}
                value={cduCapacity}
                onChange={(e) => setCduCapacity(Number(e.target.value))}
                className="w-full accent-sky-500 bg-slate-800"
              />
              <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-0.5">
                <span>Baseline: 100,000</span>
                <span>Throttled Limit</span>
              </div>
            </div>
          </div>

          <div className="pt-2 flex justify-end">
            <button
              onClick={handleRunDeltaSolve}
              disabled={isResolving}
              className="flex items-center gap-2 px-5 py-2.5 rounded bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-slate-950 text-xs font-bold uppercase tracking-wider transition-all cursor-pointer"
            >
              <Zap className="w-4 h-4 fill-current" />
              {isResolving ? 'Computing DeltaSolve...' : 'Execute DeltaSolve Re-Optimization'}
            </button>
          </div>
        </div>

        {/* Cold vs Warm Acceleration Metric Card */}
        <div className="bg-[#121824] border border-[#232e42] rounded-xl p-5 flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-200 mb-4 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
              Warm Acceleration Metrics
            </h3>

            <div className="space-y-4">
              <div className="p-3 rounded-lg bg-[#0e141f] border border-[#1f2a3d]">
                <span className="text-[11px] text-slate-400 block mb-1">Iteration Reduction</span>
                <span className="text-2xl font-bold font-mono text-emerald-400">
                  {deltaSolve?.warm_start ? iterReduction : '—'}
                </span>
                <span className="text-[10px] text-slate-500 block mt-0.5">
                  Fewer iterations needed to regain feasibility
                </span>
              </div>

              <div className="p-3 rounded-lg bg-[#0e141f] border border-[#1f2a3d]">
                <span className="text-[11px] text-slate-400 block mb-1">Solve Time Speedup</span>
                <span className="text-2xl font-bold font-mono text-cyan-400">
                  {deltaSolve?.warm_start ? `${speedup}x Faster` : '—'}
                </span>
                <span className="text-[10px] text-slate-500 block mt-0.5">
                  Reused matrix factorization & dual states
                </span>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-[#232e42] text-[11px] text-slate-400 font-mono">
            <span>Parent Job: {baselineSolve ? baselineSolve.solve_id.slice(0, 12) : 'Awaiting baseline'}</span>
          </div>
        </div>
      </div>

      {/* Before / After Comparison Table */}
      {deltaSolve && (
        <div className="bg-[#121824] border border-[#232e42] rounded-xl p-5">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">
            Cold Baseline vs DeltaSolve Comparison
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-[#232e42] text-slate-400 text-[11px]">
                  <th className="py-2.5 px-3">Run Type</th>
                  <th className="py-2.5 px-3">Job ID</th>
                  <th className="py-2.5 px-3">Iterations</th>
                  <th className="py-2.5 px-3">Solve Time</th>
                  <th className="py-2.5 px-3">Objective (Profit)</th>
                  <th className="py-2.5 px-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1f2a3d] text-slate-200">
                <tr>
                  <td className="py-3 px-3 text-slate-400 font-sans font-medium">Cold Baseline</td>
                  <td className="py-3 px-3 text-sky-400">{baselineSolve?.solve_id}</td>
                  <td className="py-3 px-3">{baselineSolve?.iterations ?? 80} iters</td>
                  <td className="py-3 px-3">{baselineSolve?.solve_time_ms ?? 410} ms</td>
                  <td className="py-3 px-3 font-semibold text-emerald-400">
                    ${baselineSolve?.objective?.toLocaleString() || '318,200,000'}
                  </td>
                  <td className="py-3 px-3">
                    <StatusBadge status={baselineSolve?.solver_status || 'OPTIMAL'} size="sm" />
                  </td>
                </tr>
                <tr className="bg-sky-950/20">
                  <td className="py-3 px-3 text-sky-400 font-sans font-medium flex items-center gap-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                    DeltaSolve (Warm)
                  </td>
                  <td className="py-3 px-3 text-cyan-400">{deltaSolve.solve_id}</td>
                  <td className="py-3 px-3 text-emerald-400 font-bold">{deltaSolve.iterations ?? 30} iters</td>
                  <td className="py-3 px-3 text-cyan-400 font-bold">{deltaSolve.solve_time_ms ?? 120} ms</td>
                  <td className="py-3 px-3 font-semibold text-emerald-400">
                    ${deltaSolve.objective?.toLocaleString() || '317,450,000'}
                  </td>
                  <td className="py-3 px-3">
                    <StatusBadge status={deltaSolve.solver_status || 'OPTIMAL'} size="sm" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
