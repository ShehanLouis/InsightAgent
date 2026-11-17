import React from 'react';
import { Sparkles, ShieldAlert, Settings, Database, Activity, FileSpreadsheet } from 'lucide-react';

export default function Navbar({ 
  datasetSummary, 
  onOpenAudit, 
  onOpenSettings, 
  activeTab, 
  setActiveTab,
  hasApiKey 
}) {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand & Title */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-white tracking-tight">InsightAgent</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/30 font-mono">
                v1.0 • Enterprise AI
              </span>
            </div>
            <p className="text-xs text-slate-400">Autonomous Data Analyst & Decision Intelligence</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="hidden md:flex items-center space-x-1 bg-slate-950 p-1 rounded-xl border border-slate-800 text-sm">
          <button
            onClick={() => setActiveTab('analyst')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg transition-all ${
              activeTab === 'analyst' 
                ? 'bg-blue-600 text-white shadow-md' 
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
            }`}
          >
            <Activity className="w-4 h-4" />
            <span>AI Analyst Console</span>
          </button>
          <button
            onClick={() => setActiveTab('explorer')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg transition-all ${
              activeTab === 'explorer' 
                ? 'bg-blue-600 text-white shadow-md' 
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
            }`}
          >
            <FileSpreadsheet className="w-4 h-4" />
            <span>Data Explorer</span>
          </button>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-3">
          
          {/* Dataset Status Pill */}
          <div className="hidden sm:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300">
            <Database className="w-3.5 h-3.5 text-blue-400" />
            <span className="font-medium truncate max-w-[140px]">{datasetSummary?.filename || 'superstore.csv'}</span>
            <span className="text-slate-500">•</span>
            <span className="text-slate-400">{datasetSummary ? `${datasetSummary.row_count.toLocaleString()} rows` : 'Loading...'}</span>
          </div>

          {/* Instant Auto-Audit Button */}
          <button
            onClick={onOpenAudit}
            className="flex items-center space-x-2 px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-amber-500 to-rose-600 hover:from-amber-600 hover:to-rose-700 text-white text-xs font-semibold shadow-md shadow-rose-950/40 transition-all transform active:scale-95"
            title="Run instant statistical health audit"
          >
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>Auto-Audit Briefing</span>
          </button>

          {/* Settings Button */}
          <button
            onClick={onOpenSettings}
            className={`p-2 rounded-lg border transition-all ${
              hasApiKey 
                ? 'border-emerald-500/40 text-emerald-400 bg-emerald-500/10 hover:bg-emerald-500/20' 
                : 'border-slate-700 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
            title="Settings & API Key"
          >
            <Settings className="w-4 h-4" />
          </button>

        </div>
      </div>
    </header>
  );
}
