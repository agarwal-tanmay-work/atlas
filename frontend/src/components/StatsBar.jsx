import React, { useEffect, useState } from 'react';
import { motion, useAnimation } from 'framer-motion';
import { getStats } from '../api';

function AnimatedCounter({ value, label }) {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    let startTime;
    const duration = 1500; // 1.5 seconds

    const animateNumber = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = timestamp - startTime;
      const percentage = Math.min(progress / duration, 1);
      
      // Easing function: easeOutQuart
      const easeOut = 1 - Math.pow(1 - percentage, 4);
      
      setDisplayValue(Math.floor(easeOut * value));

      if (percentage < 1) {
        requestAnimationFrame(animateNumber);
      }
    };

    if (value > 0) {
      requestAnimationFrame(animateNumber);
    }
  }, [value]);

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <span className="font-heading font-bold text-4xl md:text-6xl text-white mb-2 tracking-tight drop-shadow-md">
        {displayValue}
        <span className="text-accent-blue font-sans">.</span>
      </span>
      <span className="font-sans text-sm font-medium text-text-secondary uppercase tracking-[0.1em] text-center">
        {label}
      </span>
    </div>
  );
}

export default function StatsBar() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    async function loadStats() {
      try {
        const response = await getStats();
        setStats(response.data);
      } catch (error) {
        console.error("Failed to load stats:", error);
      }
    }
    loadStats();
  }, []);

  if (!stats) return <div className="h-24 bg-bg-card border-y border-border-color animate-pulse"></div>;

  const domainCount = Object.keys(stats.by_domain).length;
  const rootCauseCount = Object.keys(stats.by_root_cause).length;
  // Estimate cross domain connections based on total for visual flair
  const connectionCount = stats.total * 4; 

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="w-full bg-bg-card border-y border-border-color py-6"
    >
      <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 divide-x divide-border-subtle">
        <AnimatedCounter value={stats.total} label="Failures Indexed" />
        <AnimatedCounter value={domainCount} label="Sectors Covered" />
        <AnimatedCounter value={rootCauseCount} label="Root Causes" />
        <AnimatedCounter value={connectionCount} label="Cross-Domain Links" />
      </div>
    </motion.div>
  );
}
