import React, { useState } from 'react';
import { analyzeProject } from '../api';
import FailureCard from '../components/FailureCard';
import RootCauseTag from '../components/RootCauseTag';

export default function AnalyzePage() {
  const [description, setDescription] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [loadingText, setLoadingText] = useState('');

  const loadingMessages = [
    "Scanning 60+ historical failures...",
    "Embedding project description...",
    "Querying vector database...",
    "Identifying analogous patterns...",
    "Consulting the Atlas...",
    "Generating risk profile...",
    "Synthesizing mitigations..."
  ];

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!description.trim()) return;

    setIsAnalyzing(true);
    setResult(null);

    // Cycle through loading messages
    let msgIndex = 0;
    setLoadingText(loadingMessages[0]);
    const interval = setInterval(() => {
      msgIndex = (msgIndex + 1) % loadingMessages.length;
      setLoadingText(loadingMessages[msgIndex]);
    }, 1500);

    try {
      const response = await analyzeProject(description);
      setResult(response.data);
    } catch (err) {
      console.error(err);
      alert("Analysis failed. Check console.");
    } finally {
      clearInterval(interval);
      setIsAnalyzing(false);
    }
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'Critical': return 'bg-severity-critical text-white';
      case 'High': return 'bg-severity-high text-white';
      case 'Medium': return 'bg-severity-medium text-black';
      case 'Low': return 'bg-severity-low text-black';
      default: return 'bg-gray-500 text-white';
    }
  };

  const copyMarkdown = () => {
    if (!result) return;
    const md = `
# Project Risk Analysis: ${result.overall_risk_level} Risk

**Risk Summary:**
${result.risk_summary}

**Most Likely Root Causes:**
${result.most_likely_root_causes.map(rc => `- ${rc}`).join('\n')}

**Warning Signs To Watch:**
${result.warning_signs_to_watch.map(ws => `- ⚠️ ${ws}`).join('\n')}

**Recommended Mitigations:**
${result.recommended_mitigations.map(rm => `- ✓ ${rm}`).join('\n')}
    `.trim();
    navigator.clipboard.writeText(md);
    alert("Copied to clipboard as Markdown!");
  };

  return (
    <div className="max-w-5xl mx-auto">
      <header className="mb-12 text-center md:text-left mt-8">
        <h1 className="font-heading font-bold text-4xl leading-tight mb-4 text-white">Project Risk Analysis</h1>
        <p className="font-sans text-lg text-text-secondary max-w-3xl">Describe your architecture or project roadmap. Atlas will map it against historical failures to highlight structural blind spots.</p>
      </header>

      {!result && !isAnalyzing && (
        <form onSubmit={handleAnalyze} className="mb-12">
          <div className="relative">
            <textarea
              className="w-full h-48 bg-bg-card backdrop-blur-md rounded-xl border border-border text-text-primary p-6 font-sans text-lg focus:border-accent-blue focus:ring-4 focus:ring-accent-blue/10 outline-none transition-all resize-none shadow-xl"
              placeholder="e.g. A microservices-based payments platform relying on..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              maxLength={2000}
            ></textarea>
            <div className="absolute bottom-4 right-6 font-mono text-xs text-text-muted">
              {description.length} / 2000
            </div>
          </div>
          <div className="mt-6 flex justify-end">
            <button 
              type="submit" 
              disabled={description.length < 20}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Analyze Project Risk
            </button>
          </div>
        </form>
      )}

      {isAnalyzing && (
        <div className="flex flex-col items-center justify-center py-32 border border-border-dashed bg-bg-card/50">
          <div className="w-16 h-16 border-4 border-bg-elevated border-t-accent-red rounded-full animate-spin mb-6"></div>
          <p className="font-mono text-accent-red tracking-widest uppercase animate-pulse">{loadingText}</p>
        </div>
      )}

      {result && (
        <div className="animate-fade-in">
          {/* Risk Banner */}
          <div className={`w-full p-6 flex flex-col md:flex-row items-center justify-between mb-8 shadow-lg ${getRiskColor(result.overall_risk_level)}`}>
            <div className="flex items-center gap-4">
              <span className="text-4xl">⚠️</span>
              <div>
                <p className="font-mono text-xs uppercase tracking-widest opacity-80 font-bold">Overall Risk Assessment</p>
                <h2 className="font-serif text-3xl">{result.overall_risk_level} Risk</h2>
              </div>
            </div>
            <div className="mt-4 md:mt-0 flex gap-4">
              <button onClick={() => {setResult(null); setDescription('');}} className="font-mono text-xs uppercase tracking-widest px-4 py-2 bg-black/20 hover:bg-black/40 transition-colors rounded">
                Analyze Another
              </button>
              <button onClick={copyMarkdown} className="font-mono text-xs uppercase tracking-widest px-4 py-2 bg-black/20 hover:bg-black/40 transition-colors rounded">
                Copy Markdown
              </button>
            </div>
          </div>

          <div className="intelligence-card p-8 mb-8 border-l-4 border-l-border-subtle">
            <h3 className="font-mono text-sm uppercase tracking-widest text-text-muted mb-4">Risk Summary</h3>
            <p className="font-serif text-xl leading-relaxed text-text-primary whitespace-pre-wrap">
              {result.risk_summary}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            <div className="intelligence-card p-6 border-t-2 border-t-accent-amber">
              <h3 className="font-mono text-sm uppercase tracking-widest text-text-muted mb-6">Most Likely Root Causes</h3>
              <ul className="space-y-4">
                {result.most_likely_root_causes.map((rc, idx) => (
                  <li key={idx} className="flex gap-3">
                    <span className="font-mono text-text-muted">{idx + 1}.</span>
                    <RootCauseTag category={rc} />
                  </li>
                ))}
              </ul>
            </div>

            <div className="intelligence-card p-6 border-t-2 border-t-accent-red bg-red-900/5">
              <h3 className="font-mono text-sm uppercase tracking-widest text-text-muted mb-6">Warning Signs to Watch</h3>
              <ul className="space-y-4">
                {result.warning_signs_to_watch.map((sign, idx) => (
                  <li key={idx} className="flex gap-3 text-text-secondary text-sm">
                    <span className="text-accent-red font-bold">⚠️</span>
                    <span>{sign}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="intelligence-card p-6 border-t-2 border-t-accent-green bg-green-900/5">
              <h3 className="font-mono text-sm uppercase tracking-widest text-text-muted mb-6">Recommended Mitigations</h3>
              <ul className="space-y-4">
                {result.recommended_mitigations.map((rec, idx) => (
                  <li key={idx} className="flex gap-3 text-text-secondary text-sm">
                    <span className="text-accent-green font-bold">✓</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="mb-16">
            <h3 className="font-serif text-3xl mb-2 text-white">Historical Analogues</h3>
            <p className="font-mono text-sm text-text-muted mb-8">Your project pattern most closely matches these historical failures.</p>
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-4 gap-4">
              {result.top_analogous_failures.map(failure => (
                <div key={failure.id} className="h-full">
                  <FailureCard failure={failure} compact={false} />
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
