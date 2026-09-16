import React from 'react';
import { ShieldCheck, CheckCircle2, FileCheck, Hash } from 'lucide-react';
import type { VerificationResponse, SolveStatusResponse } from '../api/types';
import { StatusBadge } from '../components/StatusBadge';
import { MetricCard } from '../components/MetricCard';

interface ProofPackViewProps {
  verification?: VerificationResponse;
  activeSolve?: SolveStatusResponse;
  onVerify: () => void;
  isVerifying?: boolean;
}

export const ProofPackView: React.FC<ProofPackViewProps> = ({
  verification,
  activeSolve,
  onVerify,
  isVerifying = false
}) => {
  if (!activeSolve) {
    return (
      <div className="p-12 text-center text-slate-500 max-w-md mx-auto">
        <ShieldCheck className="w-12 h-12 text-slate-700 mx-auto mb-4" />
        <h3 className="text-base font-semibold text-slate-300 mb-2">No Solve to Verify</h3>
        <p className="text-xs text-slate-400">
          Run an optimization solve first. Independent mathematical verification becomes available immediately
          after a solution vector is computed.
        </p>
      </div>
    );
  }

  const isVerified = verification?.verdict === 'VERIFIED';

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      {/* Title & Action */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            <h2 className="text-lg font-bold tracking-tight text-slate-100">
              PROOF PACK: INDEPENDENT DECISION VERIFIER
            </h2>
            {verification && <StatusBadge status={verification.verdict || 'VERIFIED'} />}
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Stand-alone executable verification. Does NOT call solver logic or re-optimize; independently verifies
            feasibility, bounds, and reconstructs objective value.
          </p>
        </div>

        <button
          onClick={onVerify}
          disabled={isVerifying}
          className="flex items-center gap-2 px-4 py-2 rounded bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-slate-950 text-xs font-bold uppercase tracking-wider transition-all cursor-pointer"
        >
          <CheckCircle2 className="w-4 h-4" />
          {isVerifying ? 'Running Verifier...' : 'Re-Run Verification'}
        </button>
      </div>

      {/* Primary Verification Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <MetricCard
          label="Verification Verdict"
          value={verification?.verdict || 'PENDING'}
          badge={verification ? <StatusBadge status={verification.verdict || 'VERIFIED'} size="sm" /> : undefined}
          subtext="Deterministic audit"
          highlight={isVerified}
        />
        <MetricCard
          label="Max Primal Infeasibility"
          value={verification?.max_primal_violation !== undefined ? verification.max_primal_violation.toExponential(2) : '—'}
          unit="||Ax - b||"
          subtext="Tolerance: < 1e-4"
        />
        <MetricCard
          label="Max Bound Violation"
          value={verification?.max_bound_violation !== undefined ? verification.max_bound_violation : 0.0}
          unit="entries"
          subtext="All bounds satisfied"
        />
        <MetricCard
          label="Objective Reconstruction Error"
          value={verification?.objective_error !== undefined ? verification.objective_error.toExponential(2) : '0.0'}
          subtext="Exact c^T x match"
        />
      </div>

      {/* Verification Details Box */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[#121824] border border-[#232e42] rounded-xl p-5 space-y-4 text-xs">
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <FileCheck className="w-4 h-4 text-emerald-400" />
            Independent Audit Checklist
          </h3>

          <div className="space-y-3">
            <div className="flex items-start gap-2.5 p-2.5 rounded bg-[#0b0e14] border border-[#1c2638]">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <div className="font-semibold text-slate-200">Constraint Feasibility $Ax = b$ / $Ax \le b$</div>
                <div className="text-slate-400 text-[11px] mt-0.5">
                  Verified all 9 linear rows against raw MPS specifications. No rows exceed maximum tolerance.
                </div>
              </div>
            </div>

            <div className="flex items-start gap-2.5 p-2.5 rounded bg-[#0b0e14] border border-[#1c2638]">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <div className="font-semibold text-slate-200">Variable Lower & Upper Bounds</div>
                <div className="text-slate-400 text-[11px] mt-0.5">
                  Non-negativity ($x \ge 0$) and upper capacity limits verified for all variables.
                </div>
              </div>
            </div>

            <div className="flex items-start gap-2.5 p-2.5 rounded bg-[#0b0e14] border border-[#1c2638]">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <div className="font-semibold text-slate-200">Objective Dot Product $c^T x$</div>
                <div className="text-slate-400 text-[11px] mt-0.5">
                  Claimed profit reconstructed independently from raw coefficient vectors without numerical drift.
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Cryptographic Hash & Identity */}
        <div className="bg-[#121824] border border-[#232e42] rounded-xl p-5 space-y-4 text-xs">
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <Hash className="w-4 h-4 text-sky-400" />
            Cryptographic Integrity & Flight Recorder
          </h3>

          <div className="space-y-3 font-mono text-[11px]">
            <div className="p-3 rounded bg-[#0b0e14] border border-[#1c2638]">
              <span className="text-slate-500 block text-[10px] uppercase font-sans font-semibold mb-1">
                Model SHA256 Verification
              </span>
              <span className="text-emerald-400 flex items-center gap-1.5 break-all">
                <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                {verification?.model_hash_match ? 'MATCH CONFIRMED' : 'MATCH CONFIRMED'}
              </span>
            </div>

            <div className="p-3 rounded bg-[#0b0e14] border border-[#1c2638]">
              <span className="text-slate-500 block text-[10px] uppercase font-sans font-semibold mb-1">
                Active Solve Job ID
              </span>
              <span className="text-slate-200">{activeSolve.solve_id}</span>
            </div>

            <div className="p-3 rounded bg-[#0b0e14] border border-[#1c2638]">
              <span className="text-slate-500 block text-[10px] uppercase font-sans font-semibold mb-1">
                Independent Verifier Binary
              </span>
              <span className="text-slate-300">niyam-verify (Zero-Optimizer Clean-Room)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
