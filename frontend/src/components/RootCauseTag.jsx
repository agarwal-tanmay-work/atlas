import React from 'react';

const CATEGORY_COLORS = {
  "Communication Breakdown": "bg-yellow-500/20 text-yellow-500 border border-yellow-500/30",
  "Single Point of Failure": "bg-red-500/20 text-red-500 border border-red-500/30",
  "Incentive Misalignment": "bg-purple-500/20 text-purple-400 border border-purple-500/30",
  "Over-Complexity": "bg-indigo-500/20 text-indigo-400 border border-indigo-500/30",
  "Ignored Warning Signs": "bg-orange-500/20 text-orange-500 border border-orange-500/30",
  "Human Error": "bg-blue-500/20 text-blue-400 border border-blue-500/30",
  "Process Failure": "bg-slate-500/20 text-slate-400 border border-slate-500/30",
  "Technical Debt": "bg-zinc-600/20 text-zinc-400 border border-zinc-600/30",
  "Scaling Failure": "bg-cyan-500/20 text-cyan-400 border border-cyan-500/30",
  "Security Negligence": "bg-rose-500/20 text-rose-500 border border-rose-500/30",
  "Leadership Failure": "bg-amber-600/20 text-amber-500 border border-amber-600/30",
  "External Dependency Failure": "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30",
};

export default function RootCauseTag({ category }) {
  const colorClass = CATEGORY_COLORS[category] || "bg-gray-800 text-gray-400 border border-gray-600";
  
  return (
    <span className={`inline-flex items-center px-2 py-1 rounded-sm text-xs font-mono uppercase tracking-wider ${colorClass}`}>
      <span className="opacity-70 mr-1.5">▪</span> {category}
    </span>
  );
}
