import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getFailure } from '../api';
import DomainBadge from '../components/DomainBadge';
import RootCauseTag from '../components/RootCauseTag';
import FailureCard from '../components/FailureCard';

export default function FailurePage() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const res = await getFailure(id);
        setData(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
    window.scrollTo(0, 0);
  }, [id]);

  if (loading) return <div className="text-center py-20 font-mono text-accent-red animate-pulse">Decrypting archives...</div>;
  if (!data) return <div className="text-center py-20 font-mono text-text-muted">Record not found.</div>;

  const { failure, related_failures } = data;

  const SEVERITY_COLORS = {
    'Critical': 'bg-severity-critical shadow-[0_0_8px_rgba(255,59,59,0.8)]',
    'High': 'bg-severity-high shadow-[0_0_8px_rgba(255,122,0,0.8)]',
    'Medium': 'bg-severity-medium shadow-[0_0_8px_rgba(255,184,0,0.8)]',
    'Low': 'bg-severity-low shadow-[0_0_8px_rgba(0,214,143,0.8)]',
  };

  return (
    <div className="max-w-4xl mx-auto">
      <Link to="/search" className="font-mono text-xs text-text-muted hover:text-white mb-8 inline-block">← Back to Search</Link>
      
      {/* Header */}
      <header className="mb-12">
        <div className="flex flex-wrap items-center gap-3 mb-4">
          <DomainBadge domain={failure.domain} />
          <div className="flex items-center gap-2 border border-border-subtle px-2 py-1 rounded bg-bg-card">
            <span className={`w-2 h-2 rounded-full ${SEVERITY_COLORS[failure.severity] || 'bg-gray-500'}`}></span>
            <span className="text-xs font-mono uppercase text-text-secondary tracking-widest">{failure.severity}</span>
          </div>
          <span className="font-mono text-xs text-text-muted uppercase border border-border-color px-2 py-1 rounded">{failure.year || 'Unknown Year'}</span>
          <span className="font-mono text-xs text-text-muted uppercase border border-border-color px-2 py-1 rounded">{failure.organization || 'Unknown Org'}</span>
        </div>
        
        <h1 className="font-serif text-4xl md:text-6xl text-white leading-tight mb-4">{failure.title}</h1>
        
        {failure.source_url && (
          <a href={failure.source_url} target="_blank" rel="noreferrer" className="text-xs font-mono text-accent-blue hover:underline">
            View Primary Source ↗
          </a>
        )}
      </header>

      {/* At-a-glance */}
      <div className="bg-bg-card border border-border-color p-6 mb-12 flex flex-col md:flex-row gap-6 items-start">
        <div className="flex-1">
          <h3 className="font-mono text-xs text-text-muted uppercase tracking-widest mb-2">What Failed</h3>
          <p className="font-serif text-xl leading-relaxed">{failure.what_failed}</p>
        </div>
        <div className="w-full md:w-1/3 shrink-0">
          <h3 className="font-mono text-xs text-text-muted uppercase tracking-widest mb-2">Root Cause</h3>
          <RootCauseTag category={failure.root_cause_category} />
        </div>
      </div>

      {/* Details */}
      <div className="space-y-8 mb-16">
        <div className="intelligence-card p-6 md:p-8">
          <h2 className="font-mono text-sm uppercase tracking-widest text-text-muted mb-4 border-b border-border-subtle pb-2">The Real Root Cause</h2>
          <p className="text-text-primary leading-relaxed">{failure.root_cause}</p>
        </div>

        <div className="intelligence-card p-6 md:p-8 bg-red-900/5">
          <h2 className="font-mono text-sm uppercase tracking-widest text-text-muted mb-4 border-b border-red-900/30 pb-2 flex items-center gap-2">
            <span className="text-accent-red">⚠️</span> Warning Signs That Were Ignored
          </h2>
          <ul className="space-y-3">
            {failure.warning_signs.map((sign, i) => (
              <li key={i} className="flex gap-3 text-text-secondary">
                <span className="text-accent-red mt-1 font-bold">→</span>
                <span>{sign}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="intelligence-card p-6">
            <h2 className="font-mono text-sm uppercase tracking-widest text-text-muted mb-4 border-b border-border-subtle pb-2">What Was Done Wrong</h2>
            <p className="text-text-secondary text-sm leading-relaxed">{failure.what_was_done_wrong}</p>
          </div>
          <div className="intelligence-card p-6">
            <h2 className="font-mono text-sm uppercase tracking-widest text-text-muted mb-4 border-b border-border-subtle pb-2">How It Was Fixed</h2>
            <p className="text-text-secondary text-sm leading-relaxed">{failure.how_it_was_fixed || 'N/A - The damage was permanent.'}</p>
          </div>
        </div>

        <div className="my-12 relative py-8 px-6 border-l-4 border-accent-purple bg-gradient-to-r from-accent-purple/10 to-transparent">
          <h2 className="font-mono text-sm uppercase tracking-widest text-accent-purple mb-4">The Lesson</h2>
          <p className="font-serif text-3xl italic text-white leading-relaxed">
            "{failure.lesson}"
          </p>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2">
          {failure.tags.map(tag => (
            <span key={tag} className="bg-bg-elevated border border-border-color text-text-muted px-3 py-1 rounded-sm font-mono text-xs uppercase tracking-wider">
              #{tag}
            </span>
          ))}
        </div>
      </div>

      {/* Cross Domain */}
      {related_failures && related_failures.length > 0 && (
        <section className="pt-12 border-t border-border-color">
          <h2 className="font-serif text-2xl mb-2">Similar Failures Across Domains</h2>
          <p className="font-mono text-sm text-text-muted mb-8">These incidents share semantic similarities or root cause patterns.</p>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {related_failures.map(rf => (
              <FailureCard key={rf.id} failure={rf} compact={true} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
