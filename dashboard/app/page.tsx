"use client";

import { useState, useEffect } from 'react';

type CostSummary = {
  total_requests: number;
  total_tokens: number;
  total_cost_usd: number;
  average_latency_ms: number;
};

export default function Home(){

  const [summary, setSummary] = useState<CostSummary | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/costs/summary") //http://127.0.0.1:8000/cost/summary'
    .then((res) => res.json())
    .then((data) => setSummary(data))
    .catch((err) => console.error(err));
  }, []);

  return (
    <main className='min-h-screen bg-slate-950 text-white p-8'>
      <h1 className='text-4xl font-bold mb=2'>CostLens</h1>
      <p className="text-slate-400 mb-8">
        AI inference cost intelligence dashboard
      </p>

      {!summary ? (
        <p>Loading Dashboard...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="rounded-xl bg-slate-900 p-5">
            <p className="text-slate-400">Total Requests</p>
            <h2 className="text-3xl font-bold">{summary.total_requests}</h2>
          </div>
          <div className="rounded-xl bg-slate-900 p-5">
            <p className="text-slate-400">Total Tokens</p>
            <h2 className="text-3xl font-bold">{summary.total_tokens}</h2>
          </div>
          <div className="rounded-xl bg-slate-900 p-5">
            <p className="text-slate-400">Total Cost</p>
            <h2 className="text-3xl font-bold">${summary.total_cost_usd}</h2>
          </div>
          <div className="rounded-xl bg-slate-900 p-5">
            <p className="text-slate-400">Average Latency</p>
            <h2 className="text-3xl font-bold">{summary.average_latency_ms} ms</h2>
          </div>
        </div>
      )}
    </main>
  )
}
