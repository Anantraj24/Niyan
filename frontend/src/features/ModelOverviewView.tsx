import React, { useState } from 'react';
import { Layers, Shield, Zap, RefreshCw, CheckCircle2, Upload, Plus, X, FileText, AlertCircle } from 'lucide-react';
import type { ModelDetail, AnalysisResponse } from '../api/types';
import { MetricCard } from '../components/MetricCard';
import { StatusBadge } from '../components/StatusBadge';
import { uploadModel } from '../api/client';

interface ModelOverviewViewProps {
  model?: ModelDetail;
  analysis?: AnalysisResponse;
  onRunXRay: () => void;
  onGoToAutopilot: () => void;
  onGoToSolve: () => void;
  onModelImported?: (newModelId: string) => void;
  isAnalyzing?: boolean;
}

export const ModelOverviewView: React.FC<ModelOverviewViewProps> = ({
  model,
  analysis,
  onRunXRay,
  onGoToSolve,
  onModelImported,
  isAnalyzing = false
}) => {
  const [isImportModalOpen, setIsImportModalOpen] = useState(false);
  const [importFile, setImportFile] = useState<File | null>(null);
  const [importName, setImportName] = useState('');
  const [datasetKind, setDatasetKind] = useState('user');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const f = e.target.files[0];
      setImportFile(f);
      if (!importName) {
        setImportName(f.name.replace(/\.[^/.]+$/, '').replace(/_/g, ' '));
      }
    }
  };

  const handleUploadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!importFile) {
      setUploadError('Please choose an MPS or LP formulation file.');
      return;
    }
    setIsUploading(true);
    setUploadError(null);
    try {
      const res = await uploadModel(importFile, importName || undefined, datasetKind);
      setIsImportModalOpen(false);
      setImportFile(null);
      setImportName('');
      if (onModelImported) {
        onModelImported(res.model_id);
      }
    } catch (err: any) {
      setUploadError(err.message || 'Failed to upload formulation');
    } finally {
      setIsUploading(false);
    }
  };

  if (!model) {
    return (
      <div className="p-8 text-center text-slate-500">
        No model selected. Import a model or choose a synthetic benchmark.
      </div>
    );
  }

  const profile = analysis?.profile;

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      {/* Header Banner */}
      <div className="bg-[#121824] border border-[#232e42] rounded-xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <h1 className="text-xl font-bold tracking-tight text-slate-100">{model.display_name}</h1>
            <StatusBadge status={model.dataset_kind} size="sm" />
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
              {model.current_version?.format.toUpperCase() || 'MPS'}
            </span>
          </div>
          <p className="text-xs text-slate-400 font-mono flex items-center gap-2">
            <span>Model ID: {model.model_id}</span>
            <span>•</span>
            <span>SHA256: {model.current_version?.sha256.slice(0, 16)}...</span>
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsImportModalOpen(true)}
            className="flex items-center gap-2 px-3.5 py-2 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold tracking-wider transition-colors border border-slate-700 cursor-pointer"
          >
            <Plus className="w-3.5 h-3.5 text-emerald-400" />
            Import Model
          </button>
          <button
            onClick={onRunXRay}
            disabled={isAnalyzing}
            className="flex items-center gap-2 px-3.5 py-2 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold tracking-wider transition-colors border border-slate-700 cursor-pointer disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isAnalyzing ? 'animate-spin text-sky-400' : ''}`} />
            {isAnalyzing ? 'Analyzing...' : 'Run Model X-Ray'}
          </button>
          <button
            onClick={onGoToSolve}
            className="flex items-center gap-2 px-4 py-2 rounded bg-sky-600 hover:bg-sky-500 text-slate-950 text-xs font-semibold tracking-wider transition-colors shadow-sm cursor-pointer"
          >
            <Zap className="w-3.5 h-3.5 fill-current" />
            Solve Model
          </button>
        </div>
      </div>

      {/* Primary Mathematical Profile Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard
          label="Decision Variables"
          value={profile ? profile.variables : '—'}
          unit="cols"
          subtext={profile ? `${(profile.integer_ratio * 100).toFixed(0)}% integer variables` : 'Pending analysis'}
        />
        <MetricCard
          label="Linear Constraints"
          value={profile ? profile.constraints : '—'}
          unit="rows"
          subtext={profile ? `${profile.singleton_rows} singleton bounds` : 'Pending analysis'}
        />
        <MetricCard
          label="Nonzero Elements"
          value={profile ? profile.nonzeros : '—'}
          unit="entries"
          subtext={profile ? `Density: ${(profile.density * 100).toFixed(4)}%` : 'Pending analysis'}
          highlight
        />
        <MetricCard
          label="Formulation Risk"
          value={analysis?.risk.level || 'UNANALYZED'}
          badge={analysis ? <StatusBadge status={analysis.risk.level} size="sm" /> : undefined}
          subtext={analysis ? `${analysis.risk.issues.length} detected condition issues` : 'Run X-Ray to diagnose'}
        />
      </div>

      {/* Architecture & Verification Confidence Box */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-[#121824] border border-[#232e42] rounded-lg p-5">
          <h3 className="text-sm font-semibold text-slate-200 mb-3 flex items-center gap-2">
            <Layers className="w-4 h-4 text-sky-400" />
            Sovereignty & Numerical Path
          </h3>
          <ul className="space-y-2 text-xs text-slate-400 leading-relaxed">
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>Clean-room implementation: zero external commercial solver dependencies inside runtime.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>Deterministic Autopilot rules select CPU/CUDA acceleration based on nonzero structure.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>High-performance Ruiz equilibration & continuous PDHG solver kernel.</span>
            </li>
          </ul>
        </div>

        <div className="bg-[#121824] border border-[#232e42] rounded-lg p-5">
          <h3 className="text-sm font-semibold text-slate-200 mb-3 flex items-center gap-2">
            <Shield className="w-4 h-4 text-emerald-400" />
            Independent Decision Verification
          </h3>
          <p className="text-xs text-slate-400 mb-3 leading-relaxed">
            Every solution returned by NIYAM-X is paired with an independent Proof Pack that verifies bounds,
            constraint satisfaction, and objective reconstruction without touching the optimizer.
          </p>
          <div className="flex items-center gap-3 pt-2 border-t border-[#232e42] text-xs">
            <span className="text-slate-400 font-mono">Verifier binary:</span>
            <span className="text-emerald-400 font-mono font-semibold">niyam-verify (stand-alone)</span>
          </div>
        </div>
      </div>

      {/* Import Model Modal */}
      {isImportModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-[#121824] border border-[#232e42] rounded-xl max-w-lg w-full p-6 shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between border-b border-[#232e42] pb-3">
              <div className="flex items-center gap-2.5">
                <Upload className="w-5 h-5 text-sky-400" />
                <h3 className="text-base font-bold text-slate-100">Import Optimization Model</h3>
              </div>
              <button
                onClick={() => setIsImportModalOpen(false)}
                className="text-slate-400 hover:text-slate-200 p-1 rounded-md transition-colors cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleUploadSubmit} className="space-y-4 text-xs">
              {uploadError && (
                <div className="p-3 rounded bg-rose-950/50 border border-rose-800/80 text-rose-300 flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                  <span>{uploadError}</span>
                </div>
              )}

              {/* File Input Zone */}
              <div>
                <label className="block text-slate-300 font-medium mb-1.5">
                  Formulation File (.mps, .lp)
                </label>
                <div className="border-2 border-dashed border-[#232e42] hover:border-sky-500/60 rounded-lg p-5 text-center bg-[#0b0e14]/50 transition-colors">
                  <input
                    type="file"
                    id="model-file-upload"
                    accept=".mps,.lp,.bz2,.gz"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                  <label
                    htmlFor="model-file-upload"
                    className="cursor-pointer flex flex-col items-center gap-2"
                  >
                    <FileText className="w-8 h-8 text-sky-400/80" />
                    {importFile ? (
                      <div>
                        <span className="font-semibold text-slate-200 block">{importFile.name}</span>
                        <span className="text-[10px] text-slate-400">
                          {(importFile.size / 1024).toFixed(1)} KB • Click to change
                        </span>
                      </div>
                    ) : (
                      <div>
                        <span className="font-semibold text-sky-400 hover:underline">Click to browse</span>
                        <span className="text-slate-400"> or drag file here</span>
                        <span className="text-[10px] text-slate-400 block mt-1">
                          Standard MPS or LP formats
                        </span>
                      </div>
                    )}
                  </label>
                </div>
              </div>

              {/* Display Name Input */}
              <div>
                <label className="block text-slate-300 font-medium mb-1.5">
                  Display Name
                </label>
                <input
                  type="text"
                  value={importName}
                  onChange={(e) => setImportName(e.target.value)}
                  placeholder="e.g. Electric Power Grid Dispatch"
                  className="w-full bg-[#0b0e14] border border-[#232e42] rounded px-3 py-2 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-sky-500 font-medium"
                />
              </div>

              {/* Category / Kind Select */}
              <div>
                <label className="block text-slate-300 font-medium mb-1.5">
                  Dataset Category
                </label>
                <select
                  value={datasetKind}
                  onChange={(e) => setDatasetKind(e.target.value)}
                  className="w-full bg-[#0b0e14] border border-[#232e42] rounded px-3 py-2 text-slate-200 focus:outline-none focus:border-sky-500 font-medium"
                >
                  <option value="user">User Operational Model</option>
                  <option value="industrial">Industrial Infrastructure</option>
                  <option value="benchmark">Scientific Benchmark (Mittelmann / Netlib)</option>
                  <option value="synthetic">Synthetic Generator</option>
                </select>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-end gap-3 pt-3 border-t border-[#232e42]">
                <button
                  type="button"
                  onClick={() => setIsImportModalOpen(false)}
                  className="px-4 py-2 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold cursor-pointer transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isUploading || !importFile}
                  className="flex items-center gap-2 px-5 py-2 rounded bg-sky-600 hover:bg-sky-500 disabled:bg-slate-800 disabled:text-slate-600 text-slate-950 font-semibold cursor-pointer transition-all shadow-sm disabled:cursor-not-allowed"
                >
                  {isUploading ? (
                    <>
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                      Importing...
                    </>
                  ) : (
                    <>
                      <Upload className="w-3.5 h-3.5" />
                      Import Formulation
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
