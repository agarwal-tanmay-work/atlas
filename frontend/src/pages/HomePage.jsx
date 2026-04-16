import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import StatsBar from '../components/StatsBar';
import FailureCard from '../components/FailureCard';
import { getFailures, getRootCauses } from '../api';

export default function HomePage() {
  const [featuredFailures, setFeaturedFailures] = useState([]);
  const [rootCauses, setRootCauses] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    async function loadData() {
      try {
        const [failuresRes, causesRes] = await Promise.all([
          getFailures(null, 'Critical', 8, 0),
          getRootCauses()
        ]);
        setFeaturedFailures(failuresRes.data.slice(0, 6)); // Top 6 critical
        setRootCauses(causesRes.data);
      } catch (e) {
        console.error(e);
      }
    }
    loadData();
  }, []);

  // Root cause heatmap logic
  const topCauses = Object.entries(rootCauses)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 12);

  const getHeatmapColor = (count) => {
    if (count > 5) return 'bg-red-900/40 border-red-500/50';
    if (count > 3) return 'bg-red-900/20 border-red-500/30';
    if (count > 1) return 'bg-red-900/10 border-red-500/20';
    return 'bg-bg-elevated border-border-color';
  };

  return (
    <div className="flex flex-col gap-16 pb-12">
      {/* Hero Section */}
      <section className="mt-16 md:mt-28 text-center max-w-4xl mx-auto px-4 animate-fade-in">
        <h1 className="font-heading text-5xl md:text-7xl font-bold leading-tight mb-6 text-white tracking-tight drop-shadow-lg">
          The World's Architecture <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent-red to-accent-amber">Failure Index</span>
        </h1>
        <p className="font-sans text-xl text-text-secondary leading-relaxed mb-10 max-w-2xl mx-auto opacity-90">
          Atlas indexes documented engineering and architectural failures across industries. Reference historical data so your project doesn't repeat it.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <button onClick={() => navigate('/search')} className="btn-primary group h-14 w-60 text-lg">
            Search Index
            <span className="ml-2 group-hover:translate-x-1 transition-transform">→</span>
          </button>
          <button onClick={() => navigate('/analyze')} className="btn-secondary h-14 w-60 text-lg">
            Analyze Project
          </button>
        </div>
      </section>

      {/* Stats Bar */}
      <StatsBar />

      {/* Connections / Repeat Pattern Section */}
      <section className="max-w-5xl mx-auto w-full px-4">
        <h2 className="font-serif text-3xl mb-8 text-center border-b border-border-subtle pb-6">
          The Same Mistakes. <span className="text-text-muted">Different Industries.</span>
        </h2>
        
        <div className="intelligence-card p-6 md:p-8 bg-gradient-to-r from-bg-card to-bg-elevated relative overflow-hidden">
          <div className="absolute right-0 top-0 w-64 h-64 bg-accent-red/5 rounded-full blur-3xl mix-blend-screen pointer-events-none"></div>
          
          <p className="font-mono text-sm text-text-muted mb-6 uppercase tracking-widest text-center">Observed Pattern Match</p>
          
          <div className="flex flex-col md:flex-row items-center justify-between gap-4 relative">
            <div className="hidden md:block absolute top-1/2 left-0 w-full h-px bg-gradient-to-r from-transparent via-accent-red/40 to-transparent -translate-y-1/2 z-0"></div>
            
            <div className="bg-bg-card p-4 border border-border-color z-10 w-full md:w-1/3 text-center">
              <span className="text-xs font-mono text-accent-cyan uppercase mb-2 block">Space</span>
              <p className="font-serif text-xl">Challenger (1986)</p>
            </div>

            <div className="z-10 bg-bg-primary px-4 py-2 border border-accent-red text-accent-red font-mono text-xs uppercase tracking-widest shadow-[0_0_10px_rgba(255,59,59,0.2)]">
              Ignored Warning Signs
            </div>
            
            <div className="bg-bg-card p-4 border border-border-color z-10 w-full md:w-1/3 text-center">
              <span className="text-xs font-mono text-accent-amber uppercase mb-2 block">Finance</span>
              <p className="font-serif text-xl">Enron (2001)</p>
            </div>

            <div className="hidden md:block z-10 bg-bg-primary px-4 py-2 border border-accent-red text-accent-red font-mono text-xs uppercase tracking-widest shadow-[0_0_10px_rgba(255,59,59,0.2)]">
              Ignored Warning Signs
            </div>

            <div className="bg-bg-card p-4 border border-border-color z-10 w-full md:w-1/3 text-center">
              <span className="text-xs font-mono text-accent-purple uppercase mb-2 block">Aviation</span>
              <p className="font-serif text-xl">Boeing MAX (2019)</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Carousel */}
      <section className="w-full relative px-4">
        <div className="flex justify-between items-end mb-6">
          <h2 className="font-serif text-3xl">Highlighted Failures</h2>
          <Link to="/search" className="font-mono text-sm text-text-muted hover:text-white flex items-center">
            View All <span className="ml-1">→</span>
          </Link>
        </div>
        
        <div className="flex overflow-x-auto pb-8 -mx-4 px-4 gap-6 snap-x hide-scrollbar">
          {featuredFailures.map(f => (
            <div key={f.id} className="min-w-[320px] max-w-[320px] md:min-w-[380px] snap-center shrink-0">
              <FailureCard failure={f} />
            </div>
          ))}
          {featuredFailures.length === 0 && (
            <div className="w-full text-center py-12 text-text-muted font-mono">Loading telemetry...</div>
          )}
        </div>
      </section>

      {/* Heatmap Grid */}
      <section className="px-4">
        <h2 className="font-serif text-3xl mb-8">Root Cause Heatmap</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {topCauses.map(([cause, count]) => (
            <div 
              key={cause} 
              onClick={() => navigate(`/search?root_cause=${encodeURIComponent(cause)}`)}
              className={`p-5 cursor-pointer border ${getHeatmapColor(count)} hover:border-accent-red transition-all flex flex-col justify-between min-h-[120px]`}
            >
              <h3 className="font-mono text-sm font-bold text-white mb-4 uppercase leading-snug">{cause}</h3>
              <div className="flex justify-between items-end">
                <span className="text-3xl font-serif text-white opacity-80">{count}</span>
                <span className="text-[10px] text-text-muted tracking-widest font-mono uppercase">Incidents</span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
