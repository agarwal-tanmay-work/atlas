import React from 'react';
import { Link } from 'react-router-dom';
import DomainBadge from './DomainBadge';
import RootCauseTag from './RootCauseTag';

const SEVERITY_COLORS = {
  'Critical': 'bg-severity-critical shadow-[0_0_8px_rgba(255,59,59,0.8)]',
  'High': 'bg-severity-high shadow-[0_0_8px_rgba(255,122,0,0.8)]',
  'Medium': 'bg-severity-medium shadow-[0_0_8px_rgba(255,184,0,0.8)]',
  'Low': 'bg-severity-low shadow-[0_0_8px_rgba(0,214,143,0.8)]',
};

export default function FailureCard({ failure, similarityScore, matchReason, compact }) {
  if (!failure) return null;

  const severityDot = SEVERITY_COLORS[failure.severity] || 'bg-gray-500';

  if (compact) {
    return (
      <Link to={`/failure/${failure.id}`} className="block intelligence-card p-4 hover:bg-bg-elevated cursor-pointer h-full">
        <div className="flex items-center justify-between mb-3">
          <DomainBadge domain={failure.domain} />
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${severityDot}`}></span>
          </div>
        </div>
        <h3 className="font-serif text-lg leading-tight mb-2 text-text-primary group-hover:text-accent-red transition-colors">
          {failure.title}
        </h3>
        <div className="flex justify-between items-center mt-4">
          <span className="text-xs font-mono text-text-muted">{failure.year || 'Unknown Year'}</span>
          <RootCauseTag category={failure.root_cause_category} />
        </div>
      </Link>
    );
  }

  return (
    <Link to={`/failure/${failure.id}`} className="block intelligence-card p-5 hover:bg-bg-elevated cursor-pointer group flex flex-col h-full">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <DomainBadge domain={failure.domain} />
          <span className="text-xs font-mono text-text-muted border border-border-subtle px-2 py-0.5 rounded uppercase tracking-widest hidden sm:inline-block">
            {failure.organization || 'Unknown Org'}
          </span>
        </div>
        <div className="flex items-center gap-2 border border-border-subtle px-2 py-1 rounded bg-bg-primary/50">
          <span className={`w-2 h-2 rounded-full ${severityDot}`}></span>
          <span className="text-xs font-mono uppercase text-text-secondary tracking-widest">{failure.severity}</span>
        </div>
      </div>

      <h3 className="font-heading font-semibold text-2xl leading-tight mb-3 text-white group-hover:text-accent-blue transition-colors">
        {failure.title}
      </h3>

      <div className="mb-4">
        <RootCauseTag category={failure.root_cause_category} />
      </div>

      <p className="font-sans text-sm text-text-secondary line-clamp-2 leading-relaxed mb-4 flex-grow border-l-2 border-border-subtle pl-3">
        "{failure.lesson}"
      </p>

      {similarityScore && (
        <div className="mt-2 mb-4 bg-accent-red/10 border border-accent-red/20 px-3 py-2 rounded text-xs font-mono text-accent-red">
          <span className="font-bold mr-2">{(similarityScore * 100).toFixed(0)}% MATCH</span>
          <span className="opacity-80">{matchReason}</span>
        </div>
      )}

      <div className="flex items-center justify-between mt-auto pt-4 border-t border-border-subtle">
        <span className="text-xs font-mono text-text-muted">{failure.year || 'N/A'}</span>
        <div className="flex gap-2 w-full justify-end overflow-hidden ml-4">
          {failure.tags.slice(0, 3).map((tag, i) => (
            <span key={i} className="text-[10px] font-mono text-text-muted bg-bg-primary px-1.5 py-0.5 rounded whitespace-nowrap overflow-hidden text-ellipsis">
              #{tag}
            </span>
          ))}
        </div>
      </div>
    </Link>
  );
}
