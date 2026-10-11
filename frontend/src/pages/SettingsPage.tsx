import React from 'react';
import { Cpu, Server, CheckCircle2, AlertTriangle } from 'lucide-react';
import { HealthInfo } from '../types';

interface SettingsPageProps {
  health?: HealthInfo;
}

export const SettingsPage: React.FC<SettingsPageProps> = ({ health }) => {
  return (
    <div className="max-w-4xl mx-auto px-6 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-display font-bold text-white">System Settings & Hardware Profile</h1>
        <p className="text-sm text-slate-400 mt-1">
          Monitor your local machine hardware allocation, speech-to-text models, and local LLM connectivity.
        </p>
      </div>

      {/* Hardware Profile Card */}
      <div className="glass-panel p-6 rounded-2xl border border-surface-700/80 space-y-5">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-brand-500/10 flex items-center justify-center text-brand-400">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-white">Detected Hardware & Resource Profile</h2>
            <p className="text-xs text-slate-400">Adaptive resource allocation for zero crashes on long videos</p>
          </div>
        </div>

        {health ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2">
            <div className="bg-surface-800/80 p-3.5 rounded-xl border border-surface-700">
              <span className="text-[11px] text-slate-400 block mb-1">Hardware Tier</span>
              <span className="text-sm font-semibold text-brand-400 uppercase">
                {health.hardware.profile} Tier
              </span>
            </div>
            <div className="bg-surface-800/80 p-3.5 rounded-xl border border-surface-700">
              <span className="text-[11px] text-slate-400 block mb-1">Processor Threads</span>
              <span className="text-sm font-semibold text-white">
                {health.hardware.cpu_logical_cores} Cores
              </span>
            </div>
            <div className="bg-surface-800/80 p-3.5 rounded-xl border border-surface-700">
              <span className="text-[11px] text-slate-400 block mb-1">Available Memory</span>
              <span className="text-sm font-semibold text-white">
                {health.hardware.memory_available_gb} / {health.hardware.memory_total_gb} GB
              </span>
            </div>
            <div className="bg-surface-800/80 p-3.5 rounded-xl border border-surface-700">
              <span className="text-[11px] text-slate-400 block mb-1">Free Storage (D:)</span>
              <span className="text-sm font-semibold text-emerald-400">
                {health.storage.free_space_gb} GB Free
              </span>
            </div>
          </div>
        ) : (
          <p className="text-xs text-slate-400">Loading hardware metrics...</p>
        )}
      </div>

      {/* AI Engine Configuration Card */}
      <div className="glass-panel p-6 rounded-2xl border border-surface-700/80 space-y-5">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 flex items-center justify-center text-indigo-400">
            <Server className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-white">AI Engine & Model Setup</h2>
            <p className="text-xs text-slate-400">Local models running private and offline on your computer</p>
          </div>
        </div>

        <div className="space-y-4 pt-1">
          {/* Whisper */}
          <div className="flex items-center justify-between p-3.5 bg-surface-800/80 rounded-xl border border-surface-700">
            <div>
              <span className="text-sm font-medium text-white block">faster-whisper (Speech-to-Text)</span>
              <span className="text-xs text-slate-400">
                Active model: <code className="text-brand-400">{health?.ai_providers.whisper_model || 'base'}</code> (Device: {health?.ai_providers.whisper_device || 'cpu'}, Compute: {health?.ai_providers.whisper_compute_type || 'int8'})
              </span>
            </div>
            <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-lg">
              Optimal for 8GB RAM
            </span>
          </div>

          {/* Ollama */}
          <div className="flex items-center justify-between p-3.5 bg-surface-800/80 rounded-xl border border-surface-700">
            <div>
              <span className="text-sm font-medium text-white block">Ollama (Local LLM Q&A)</span>
              <span className="text-xs text-slate-400">
                Endpoint: <code className="text-slate-300">{health?.ai_providers.ollama_base_url || 'http://127.0.0.1:11434'}</code> (Model: {health?.ai_providers.ollama_model || 'llama3.2:1b'})
              </span>
            </div>
            {health?.ai_providers.ollama_active ? (
              <span className="flex items-center gap-1.5 text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-lg">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Connected</span>
              </span>
            ) : (
              <span className="flex items-center gap-1.5 text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2.5 py-1 rounded-lg">
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>Fallback Mode Active</span>
              </span>
            )}
          </div>

          {/* Embeddings */}
          <div className="flex items-center justify-between p-3.5 bg-surface-800/80 rounded-xl border border-surface-700">
            <div>
              <span className="text-sm font-medium text-white block">Semantic Embeddings</span>
              <span className="text-xs text-slate-400">
                Model: <code className="text-slate-300">{health?.ai_providers.embedding_model || 'all-MiniLM-L6-v2'}</code> (Fast CPU generation)
              </span>
            </div>
            <span className="text-xs bg-brand-500/10 text-brand-300 border border-brand-500/20 px-2.5 py-1 rounded-lg">
              384 Dimensions
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
