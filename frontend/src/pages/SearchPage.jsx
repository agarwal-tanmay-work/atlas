import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import FailureCard from '../components/FailureCard';
import { searchFailures, searchBySymptom, getDomains, getRootCauses } from '../api';

export default function SearchPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const queryParams = new URLSearchParams(location.search);
  
  const initialQ = queryParams.get('q') || '';
  const initialDomain = queryParams.get('domain') || '';
  const initialRootCause = queryParams.get('root_cause') || '';

  const [query, setQuery] = useState(initialQ);
  const [domainFilter, setDomainFilter] = useState(initialDomain);
  const [rcFilter, setRcFilter] = useState(initialRootCause);
  const [searchMode, setSearchMode] = useState('semantic'); // semantic or symptom

  const [results, setResults] = useState([]);
  const [insight, setInsight] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const [availableDomains, setAvailableDomains] = useState([]);
  const [availableRcs, setAvailableRcs] = useState([]);

  useEffect(() => {
    Promise.all([getDomains(), getRootCauses()]).then(([dRes, rcRes]) => {
      setAvailableDomains(Object.keys(dRes.data));
      setAvailableRcs(Object.keys(rcRes.data));
    });
  }, []);

  useEffect(() => {
    if (initialQ || initialDomain || initialRootCause) {
      handleSearch(null, initialQ, initialDomain, initialRootCause);
    }
  }, []);

  const handleSearch = async (e, q = query, d = domainFilter, rc = rcFilter) => {
    if (e) e.preventDefault();
    if (!q && !d && !rc) return;

    setIsLoading(true);
    setHasSearched(true);
    setInsight(null);
    setResults([]);

    // Update URL
    const params = new URLSearchParams();
    if (q) params.set('q', q);
    if (d) params.set('domain', d);
    if (rc) params.set('root_cause', rc);
    navigate({ search: params.toString() }, { replace: true });

    try {
      let res;
      if (searchMode === 'symptom' && q) {
        res = await searchBySymptom(q);
      } else {
        res = await searchFailures(q || 'failure', d || null, rc || null, 12);
      }
      setResults(res.data.results || []);
      setInsight(res.data.cross_domain_insight);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col md:flex-row gap-8">
      {/* Sidebar Filters */}
      <aside className="w-full md:w-64 shrink-0 space-y-6">
        <div>
          <h3 className="font-mono text-xs text-text-muted uppercase tracking-widest mb-3">Search Mode</h3>
          <div className="flex bg-bg-elevated p-1 rounded">
            <button 
              type="button"
              className={`flex-1 text-xs font-mono py-2 ${searchMode === 'semantic' ? 'bg-bg-primary text-white border border-border-color' : 'text-text-muted'}`}
              onClick={() => setSearchMode('semantic')}
            >Semantic</button>
            <button 
              type="button"
              className={`flex-1 text-xs font-mono py-2 ${searchMode === 'symptom' ? 'bg-bg-primary text-white border border-border-color' : 'text-text-muted'}`}
              onClick={() => setSearchMode('symptom')}
            >Symptom</button>
          </div>
        </div>

        <div>
          <h3 className="font-mono text-xs text-text-muted uppercase tracking-widest mb-3">Filter by Domain</h3>
          <select 
            className="w-full bg-bg-elevated border border-border-color text-text-primary text-sm p-2 outline-none focus:border-accent-red font-mono"
            value={domainFilter}
            onChange={(e) => setDomainFilter(e.target.value)}
          >
            <option value="">Any Domain</option>
            {availableDomains.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        </div>

        <div>
          <h3 className="font-mono text-xs text-text-muted uppercase tracking-widest mb-3">Filter by Root Cause</h3>
          <select 
            className="w-full bg-bg-elevated border border-border-color text-text-primary text-sm p-2 outline-none focus:border-accent-red font-mono"
            value={rcFilter}
            onChange={(e) => setRcFilter(e.target.value)}
          >
            <option value="">Any Root Cause</option>
            {availableRcs.map(rc => <option key={rc} value={rc}>{rc}</option>)}
          </select>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1">
        <form onSubmit={handleSearch} className="mb-8 relative">
          <input
            type="text"
            placeholder={searchMode === 'semantic' ? "e.g. Database migration failure..." : "e.g. Team keeps missing deadlines..."}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-bg-card backdrop-blur-md border border-border text-white text-lg lg:text-2xl font-sans p-6 pl-8 rounded-xl shadow-lg outline-none focus:border-accent-blue focus:ring-4 focus:ring-accent-blue/10 transition-all placeholder-text-muted/50"
          />
          <button type="submit" disabled={isLoading} className="absolute right-6 top-1/2 -translate-y-1/2 text-accent-blue hover:text-white disabled:opacity-50 font-sans font-medium tracking-wide transition-colors">
            {isLoading ? 'Scanning...' : 'Search'}
          </button>
        </form>

        {isLoading && (
          <div className="w-full h-32 flex items-center justify-center">
            <span className="font-mono text-accent-red animate-pulse">Running semantic analysis...</span>
          </div>
        )}

        {!isLoading && hasSearched && insight && (
          <div className="mb-8 p-6 border-l-2 border-accent-amber bg-accent-amber/5">
            <div className="flex items-center gap-2 mb-3">
              <span className="text-xl">⚡</span>
              <h3 className="font-mono text-sm tracking-widest uppercase text-accent-amber">Cross-Domain Insight</h3>
            </div>
            <p className="font-serif text-lg leading-relaxed text-white">
              {insight}
            </p>
          </div>
        )}

        {!isLoading && hasSearched && (
          <div>
            <div className="flex justify-between items-end mb-6">
              <h3 className="font-mono text-sm uppercase tracking-widest text-text-muted">{results.length} results found</h3>
            </div>
            
            {results.length > 0 ? (
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                {results.map((r) => (
                  <FailureCard key={r.failure.id} failure={r.failure} similarityScore={r.similarity_score} matchReason={r.match_reason} />
                ))}
              </div>
            ) : (
              <div className="text-center py-20 bg-bg-card border border-border-dashed">
                <p className="font-mono text-text-secondary mb-2">No historical matches found.</p>
                <p className="text-sm text-text-muted">Try removing filters or using different keywords.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
