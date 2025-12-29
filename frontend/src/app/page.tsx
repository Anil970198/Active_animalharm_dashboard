'use client';

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

const Map = dynamic(() => import('../components/Map'), { ssr: false });

export default function Home() {
  const [violations, setViolations] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchViolations = async () => {
    try {
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      const res = await fetch(`${API_BASE}/api/violations`);
      const data = await res.json();
      setViolations(data);
    } catch (e) {
      console.error("Failed to fetch violations", e);
    }
  };

  const triggerScrape = async () => {
    setLoading(true);
    try {
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      await fetch(`${API_BASE}/api/trigger-scrape`, { method: 'POST' });
      await fetchViolations();
    } catch (e) {
      alert("Scrape failed: " + e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchViolations();
  }, []);

  return (
    <div className="flex h-screen flex-col">
      <header className="bg-slate-900 text-white p-4 shadow-md z-10 flex justify-between items-center">
        <h1 className="text-xl font-bold tracking-tight">Animal Welfare Dashboard (India)</h1>
        <button
          onClick={triggerScrape}
          disabled={loading}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors disabled:opacity-50"
        >
          {loading ? 'Scraping...' : 'Refresh Data'}
        </button>
      </header>

      <main className="flex-1 relative">
        <Map violations={violations} />

        {/* Overlay Stats Card */}
        <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm p-4 rounded-lg shadow-xl z-[1000] max-w-sm">
          <h2 className="text-lg font-bold text-gray-800">Cruelty Cases (India)</h2>
          <p className="text-gray-500 text-sm mb-4">Official data from Animal Welfare Board of India.</p>
          <div className="flex gap-4">
            <div className="text-center">
              <span className="block text-2xl font-bold text-red-600">{violations.length}</span>
              <span className="text-xs text-gray-500">Active Cases</span>
            </div>
            <div className="text-center">
              <span className="block text-2xl font-bold text-gray-800">300+</span>
              <span className="text-xs text-gray-500">Total Records</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
