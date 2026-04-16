import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
  const location = useLocation();
  
  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'Search', path: '/search' },
    { name: 'Analyze', path: '/analyze' },
  ];

  return (
    <nav className="fixed top-0 w-full z-50 bg-bg-primary/90 backdrop-blur-md border-b border-border-color h-16">
      <div className="max-w-7xl mx-auto px-6 h-full flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 group">
          <span className="font-serif text-2xl tracking-wide text-white group-hover:text-gray-300 transition-colors">
            Atlas<span className="text-accent-red font-sans">.</span>
          </span>
        </Link>
        
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => {
            const isActive = location.pathname === link.path;
            return (
              <Link
                key={link.name}
                to={link.path}
                className={`font-mono text-sm tracking-widest uppercase transition-all relative py-2 ${
                  isActive ? 'text-white' : 'text-text-secondary hover:text-white'
                }`}
              >
                {link.name}
                {isActive && (
                  <span className="absolute bottom-0 left-0 w-full h-[2px] bg-accent-red shadow-[0_0_8px_rgba(255,59,59,0.8)]"></span>
                )}
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
