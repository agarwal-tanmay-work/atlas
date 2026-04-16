import React from 'react';

const DOMAIN_COLORS = {
  'Software Engineering': 'border-accent-blue text-accent-blue bg-accent-blue/10',
  'Aviation': 'border-accent-purple text-accent-purple bg-accent-purple/10',
  'Finance': 'border-accent-amber text-accent-amber bg-accent-amber/10',
  'Healthcare': 'border-accent-green text-accent-green bg-accent-green/10',
  'Government': 'border-accent-red text-accent-red bg-accent-red/10',
  'Infrastructure': 'border-orange-500 text-orange-500 bg-orange-500/10',
  'Space': 'border-teal-400 text-teal-400 bg-teal-400/10',
  'Cybersecurity': 'border-pink-500 text-pink-500 bg-pink-500/10',
  'Manufacturing': 'border-gray-400 text-gray-400 bg-gray-400/10',
  'Military': 'border-rose-700 text-rose-500 bg-rose-900/20'
};

const DEFAULT_COLOR = 'border-border-color text-text-secondary bg-bg-elevated';

export default function DomainBadge({ domain }) {
  const colorClass = DOMAIN_COLORS[domain] || DEFAULT_COLOR;
  
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-mono border uppercase tracking-wider ${colorClass}`}>
      {domain}
    </span>
  );
}
