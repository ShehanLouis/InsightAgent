import React from 'react';
import { X, ShieldAlert, AlertTriangle, AlertCircle, CheckCircle, Copy, Check } from 'lucide-react';

export default function AutoAuditModal({ isOpen, onClose, auditData }) {
  const [copied, setCopied] = React.useState(false);

  if (!isOpen || !auditData) return null;

  const handleCopy = () => {
    const text = `EXECUTIVE HEALTH AUDIT REPORT (${auditData.generated_at})
Health Score: ${auditData.health_score}/100

EXECUTIVE SUMMARY:
${auditData.executive_summary}

KEY ANOMALIES & STRATEGIC RECOMMENDATIONS:
${auditData.anomalies.map((a, i) => `${i+1}. [${a.severity.toUpperCase()}] ${a.title}
- Metric: ${a.metric} | Dimension: ${a.dimension}
- Observation: ${a.observation}
- Impact: ${a.impact}
- Recommendation: ${a.recommendation}`).join('\n\n')}
`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getSeverityBadge = (severity) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return <span className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 border border-rose-500/30 text-xs font-semibold flex items-center gap-1"><AlertTriangle className="w-3 h-3" /> Critical Risk</span>;
      case 'medium':
        return <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 text-xs font-semibold flex items-center gap-1"><AlertCircle className="w-3 h-3" /> Moderate Risk</span>;
      default:
        return <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30 text-xs font-semibold flex items-center gap-1"><CheckCircle className="w-3 h-3" /> Operational</span>;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/50">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-400">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Autonomous Executive Diagnostic Audit</h2>
              <p className="text-xs text-slate-400">Statistical Anomaly & Profit Leak Detection Engine • {auditData.generated_at}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={handleCopy}
              className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 flex items-center space-x-1.5 border border-slate-700 transition-all"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Export Briefing'}</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6">
          
          {/* Executive Score & Summary Banner */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 bg-slate-950/60 p-5 rounded-xl border border-slate-800">
            <div className="flex flex-col items-center justify-center p-3 border-b md:border-b-0 md:border-r border-slate-800 text-center">
              <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-1">Portfolio Health</span>
              <div className="text-4xl font-extrabold text-amber-400 tracking-tight">
                {auditData.health_score}<span className="text-lg text-slate-500 font-normal">/100</span>
              </div>
              <span className="text-[11px] text-rose-400 font-medium mt-1">5 Severe Anomalies</span>
            </div>
            <div className="md:col-span-3 flex flex-col justify-center">
              <span className="text-xs uppercase tracking-wider text-blue-400 font-semibold mb-1">Executive Summary</span>
              <p className="text-sm text-slate-300 leading-relaxed">
                {auditData.executive_summary}
              </p>
            </div>
          </div>

          {/* Key Drivers List */}
          {auditData.key_drivers?.length > 0 && (
            <div className="bg-slate-950/40 p-4 rounded-xl border border-slate-800/80">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Primary Margin Degradation Drivers</h3>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-slate-300">
                {auditData.key_drivers.map((driver, idx) => (
                  <li key={idx} className="flex items-start space-x-2">
                    <span className="text-rose-400 font-bold">•</span>
                    <span>{driver}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Anomaly Cards */}
          <div>
            <h3 className="text-sm font-bold text-white mb-3">Detected Anomalies & Actionable Remediation</h3>
            <div className="space-y-3">
              {auditData.anomalies.map((item, idx) => (
                <div key={idx} className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 hover:border-slate-700 transition-all">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-semibold text-white">{item.title}</span>
                    </div>
                    {getSeverityBadge(item.severity)}
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs mb-3 text-slate-400 bg-slate-900/50 p-2.5 rounded-lg border border-slate-800/60 font-mono">
                    <div><span className="text-slate-500">Metric:</span> {item.metric}</div>
                    <div><span className="text-slate-500">Dimension:</span> {item.dimension}</div>
                  </div>

                  <p className="text-xs text-slate-300 mb-2">
                    <span className="font-semibold text-slate-200">Observation:</span> {item.observation}
                  </p>
                  
                  <p className="text-xs text-rose-300/90 mb-3">
                    <span className="font-semibold text-rose-400">Business Impact:</span> {item.impact}
                  </p>

                  <div className="bg-blue-950/30 border border-blue-900/40 rounded-lg p-3 text-xs text-blue-200 flex items-start space-x-2">
                    <span className="font-bold text-blue-400 whitespace-nowrap">Recommended Action:</span>
                    <span>{item.recommendation}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-800 bg-slate-900/80 flex items-center justify-between text-xs text-slate-400">
          <span>InsightAgent Statistical Intelligence Engine</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-medium transition-all"
          >
            Close Report
          </button>
        </div>

      </div>
    </div>
  );
}
