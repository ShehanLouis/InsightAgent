import React from 'react';
import { DollarSign, TrendingUp, ShoppingBag, Users, AlertTriangle, ArrowUpRight, ArrowDownRight } from 'lucide-react';

export default function KpiBar({ summary, onOpenAudit }) {
  const kpis = summary?.quick_kpis || {};

  const totalSales = kpis.total_sales ? `$${(kpis.total_sales / 1e6).toFixed(2)}M` : '$2.30M';
  const totalProfit = kpis.total_profit ? `$${(kpis.total_profit / 1e3).toFixed(1)}K` : '$286.4K';
  const margin = kpis.profit_margin ? `${kpis.profit_margin.toFixed(1)}%` : '12.5%';
  const orders = kpis.total_orders ? kpis.total_orders.toLocaleString() : '5,009';
  const customers = kpis.unique_customers ? kpis.unique_customers.toLocaleString() : '793';

  return (
    <div className="grid grid-cols-2 md:grid-cols-6 gap-3 mb-6">
      
      {/* Total Sales */}
      <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl relative overflow-hidden group hover:border-slate-700 transition-all">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-xs font-medium uppercase tracking-wider">Gross Sales</span>
          <DollarSign className="w-4 h-4 text-blue-400" />
        </div>
        <div className="text-xl sm:text-2xl font-bold text-white tracking-tight">{totalSales}</div>
        <div className="flex items-center text-xs text-emerald-400 mt-1 font-medium">
          <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" />
          <span>+20.4% YoY</span>
        </div>
      </div>

      {/* Total Profit */}
      <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl relative overflow-hidden group hover:border-slate-700 transition-all">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-xs font-medium uppercase tracking-wider">Net Profit</span>
          <TrendingUp className="w-4 h-4 text-emerald-400" />
        </div>
        <div className="text-xl sm:text-2xl font-bold text-white tracking-tight">{totalProfit}</div>
        <div className="flex items-center text-xs text-emerald-400 mt-1 font-medium">
          <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" />
          <span>+14.2% YoY</span>
        </div>
      </div>

      {/* Blended Margin */}
      <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl relative overflow-hidden group hover:border-slate-700 transition-all">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-xs font-medium uppercase tracking-wider">Operating Margin</span>
          <span className="text-xs px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 font-mono">Target: 15%</span>
        </div>
        <div className="text-xl sm:text-2xl font-bold text-white tracking-tight">{margin}</div>
        <div className="flex items-center text-xs text-amber-400 mt-1 font-medium">
          <ArrowDownRight className="w-3.5 h-3.5 mr-0.5" />
          <span>-2.5% vs Target</span>
        </div>
      </div>

      {/* Total Orders */}
      <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl relative overflow-hidden group hover:border-slate-700 transition-all">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-xs font-medium uppercase tracking-wider">Total Orders</span>
          <ShoppingBag className="w-4 h-4 text-indigo-400" />
        </div>
        <div className="text-xl sm:text-2xl font-bold text-white tracking-tight">{orders}</div>
        <div className="text-xs text-slate-400 mt-1">Across 4 Regions</div>
      </div>

      {/* Unique Customers */}
      <div className="bg-slate-900/90 border border-slate-800 p-4 rounded-xl relative overflow-hidden group hover:border-slate-700 transition-all">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span className="text-xs font-medium uppercase tracking-wider">Client Base</span>
          <Users className="w-4 h-4 text-cyan-400" />
        </div>
        <div className="text-xl sm:text-2xl font-bold text-white tracking-tight">{customers}</div>
        <div className="text-xs text-slate-400 mt-1">Enterprise & Retail</div>
      </div>

      {/* Health Score Card */}
      <div 
        onClick={onOpenAudit}
        className="bg-gradient-to-br from-amber-950/40 via-slate-900 to-rose-950/30 border border-amber-600/40 p-4 rounded-xl relative overflow-hidden group cursor-pointer hover:border-amber-500 transition-all shadow-lg shadow-amber-950/20"
      >
        <div className="flex items-center justify-between text-amber-400 mb-1">
          <span className="text-xs font-semibold uppercase tracking-wider">Health Audit</span>
          <AlertTriangle className="w-4 h-4 text-amber-400 animate-pulse" />
        </div>
        <div className="flex items-baseline space-x-1">
          <span className="text-2xl font-black text-amber-300">39</span>
          <span className="text-xs text-amber-400/80 font-mono">/ 100</span>
        </div>
        <div className="text-[11px] text-amber-200/90 mt-1 font-medium flex items-center justify-between">
          <span>5 Risks Detected</span>
          <span className="underline group-hover:text-amber-100">View &rarr;</span>
        </div>
      </div>

    </div>
  );
}
