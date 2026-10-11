import React from 'react';
import { Cpu, HardDrive, Settings as SettingsIcon, Sparkles } from 'lucide-react';
import { HealthInfo } from '../types';

interface NavbarProps {
  currentTab: 'home' | 'workspace' | 'settings';
  setCurrentTab: (tab: 'home' | 'workspace' | 'settings') => void;
  health?: HealthInfo;
}

export const Navbar: React.FC<NavbarProps> = ({ currentTab, setCurrentTab, health }) => {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-surface-700/80 px-6 py-3.5 flex items-center justify-between">
      {/* Brand */}
      <div 
        className="flex items-center gap-3 cursor-pointer group" 
        onClick={() => setCurrentTab('home')}
      >
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center shadow-lg shadow-brand-500/25 group-hover:scale-105 transition-transform">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <div>
          <span className="font-display font-bold text-xl tracking-tight bg-gradient-to-r from-white via-slate-200 to-brand-400 bg-clip-text text-transparent">
            VidMind
          </span>
          <span className="block text-[10px] font-medium text-slate-400 tracking-wider uppercase">
            Grounded Video Intelligence
          </span>
        </div>
      </div>

      {/* Navigation tabs */}
      <nav className="flex items-center gap-1 bg-surface-800/80 p-1 rounded-xl border border-surface-700/60">
        <button
          onClick={() => setCurrentTab('home')}
          className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
            currentTab === 'home'
              ? 'bg-brand-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-slate-200 hover:bg-surface-700/50'
          }`}
        >
          Library
        </button>
        <button
          onClick={() => setCurrentTab('workspace')}
          className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
            currentTab === 'workspace'
              ? 'bg-brand-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-slate-200 hover:bg-surface-700/50'
          }`}
        >
          Workspace
        </button>
        <button
          onClick={() => setCurrentTab('settings')}
          className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
            currentTab === 'settings'
              ? 'bg-brand-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-slate-200 hover:bg-surface-700/50'
          }`}
        >
          Settings
        </button>
      </nav>

      {/* System Status Indicators */}
      <div className="flex items-center gap-3">
        {health && (
          <div className="hidden md:flex items-center gap-2.5 text-xs text-slate-400 bg-surface-800/60 px-3 py-1.5 rounded-lg border border-surface-700/50">
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>DB: OK</span>
            </span>
            <span className="text-surface-600">|</span>
            <span className="flex items-center gap-1">
              <Cpu className="w-3.5 h-3.5 text-brand-400" />
              <span>{health.hardware.profile.toUpperCase()} ({health.hardware.cpu_logical_cores}T)</span>
            </span>
            <span className="text-surface-600">|</span>
            <span className="flex items-center gap-1">
              <HardDrive className="w-3.5 h-3.5 text-slate-400" />
              <span>{health.storage.free_space_gb} GB</span>
            </span>
          </div>
        )}
        <button
          onClick={() => setCurrentTab('settings')}
          className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-surface-700/60 transition-colors"
          title="System Settings"
        >
          <SettingsIcon className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
};
