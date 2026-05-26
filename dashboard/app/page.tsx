"use client";

import { useState, useEffect } from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip
} from "recharts";

type CostSummary = {
  total_requests: number;
  total_tokens: number;
  total_cost_usd: number;
  average_latency_ms: number;
};

type FeatureCost = {
  feature: string;
  total_cost_usd: number;
};

type ModelCost = {
  model: string;
  total_cost_usd: number;
};

type Events = {
  id:  number;
  feature: string;
  model: string;
  total_tokens: number;
  estimated_cost: number;
  latency_ms: number;
};

type CacheStats = {
  total_cache_entries: number;
  total_cache_hits: number;
  estimated_saved_requests: number;
  estimated_saved_cost_usd: number;
};

export default function Home(){

  const [summary, setSummary] = useState<CostSummary | null>(null);
  const [featureCosts, setFeatureCosts] = useState<FeatureCost[]>([]);
  const [modelCosts, setModelCosts] = useState<ModelCost[]>([]);
  const [events, setEvents] = useState<Events[]>([]);
  const [cacheStats, setCacheStats] = useState<CacheStats | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/costs/summary") 
    .then((res) => res.json())
    .then((data) => setSummary(data))
    .catch((err) => console.error(err));

    fetch("http://127.0.0.1:8000/costs/by-feature")
    .then((res) => res.json())
    .then((data) => setFeatureCosts(data))
    .catch((err) => console.error(err))

    fetch("http://127.0.0.1:8000/costs/by-model")
    .then((res) => res.json())
    .then((data) => setModelCosts(data))
    .catch((err) => console.error(err))

    fetch("http://127.0.0.1:8000/events")
    .then((res) => res.json())
    .then((data) => setEvents(data))
    .catch((err) => console.error(err))
    
    fetch("http://127.0.0.1:8000/cache/stats")
    .then((res) => res.json())
    .then((data) => setCacheStats(data))
    .catch((err) => console.error(err))
    
  }, []);

  return (
    <main className='min-h-screen bg-slate-950 text-white p-8'>
      <div className="mb-10">
        <p className="text-sm text-sky-400 font-semibold mb-2">
          AI Cost Observability
        </p>

        <h1 className="text-5xl font-bold mb-3">
          CostLens
        </h1>

        <p className="text-slate-400 max-w-2xl">
          Track LLM usage, token consumption, latency, and feature-level spending from one dashboard.
        </p>
      </div>

      {!summary ? (
        <p>Loading Dashboard...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="rounded-2xl bg-slate-900 p-6 border border-slate-800">
            <p className="text-slate-400">Total Requests</p>
            <h2 className="text-3xl font-bold">{summary.total_requests}</h2>
          </div>
          <div className="rounded-2xl bg-slate-900 p-6 border border-slate-800">
            <p className="text-slate-400">Total Tokens</p>
            <h2 className="text-3xl font-bold">{summary.total_tokens}</h2>
          </div>
          <div className="rounded-2xl bg-slate-900 p-6 border border-slate-800">
            <p className="text-slate-400">Total Cost</p>
            <h2 className="text-3xl font-bold">${summary.total_cost_usd}</h2>
          </div>
          <div className="rounded-2xl bg-slate-900 p-6 border border-slate-800">
            <p className="text-slate-400">Average Latency</p>
            <h2 className="text-3xl font-bold">{summary.average_latency_ms} ms</h2>
          </div>

        </div>
      )}

      {cacheStats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
            <div className="rounded-2xl bg-slate-900 p-6 border border-slate-800">
              <p className="text-slate-400">Cache Entries</p>
              <h2 className="text-3xl font-bold">{cacheStats.total_cache_entries}</h2>
            </div>

            <div className="rounded-2xl bg-slate-900 p-6 border border-slate-800">
              <p className="text-slate-400">Cache Hits</p>
              <h2 className="text-3xl font-bold">{cacheStats.total_cache_hits}</h2>
            </div>

            <div className="rounded-2xl bg-slate-900 p-6 border border-slate-800">
              <p className="text-slate-400">Saved Requests</p>
              <h2 className="text-3xl font-bold">{cacheStats.estimated_saved_requests}</h2>
            </div>

            <div className="rounded-2xl bg-slate-900 p-6 border border-slate-800">
              <p className="text-slate-400">Estimated Saved Cost</p>
              <h2 className="text-3xl font-bold">
                ${cacheStats.estimated_saved_cost_usd}
              </h2>
            </div>
          </div>
        )
      }

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className='col-span-1 md:col-span-2 mt-10 rounded-2xl bg-slate-900 p-6 border border-slate-800'>
          <h2 className='text-2xl font-bold mb-6'>
            Cost By Feature 
          </h2>

          <div className='h-80 w-full min-w-0'>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart 
                data={featureCosts}
                margin={{
                  top: 10,
                  right: 10,
                  left: -20,
                  bottom: 20
                }}
              >
                <XAxis dataKey="feature" stroke="#94a3b8" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 10 }} stroke="#94a3b8"/>
                <Tooltip />
                <Bar
                  dataKey="total_cost_usd"
                  fill="#38bdf8"
                  radius={[6,6,0,0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>

        </div>

        <div className='col-span-1 md:col-span-2 mt-10 rounded-2xl bg-slate-900 p-6 border border-slate-800'>
          <h2 className='text-2xl font-bold mb-6'>
            Cost By Model 
          </h2>

          <div className='h-80 w-full min-w-0'>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart 
                data={modelCosts}
                margin={{
                  top: 10,
                  right: 10,
                  left: -20,
                  bottom: 20
                }}
              >
                <XAxis dataKey="model" stroke="#94a3b8" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 10 }} stroke="#94a3b8"/>
                <Tooltip />
                <Bar
                  dataKey="total_cost_usd"
                  fill="#38bdf8"
                  radius={[6,6,0,0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className='col-span-1 md:col-span-4 mt-10 rounded-xl bg-slate-900 p-6'>
        <h2 className='text-2xl font-bold mb-6'>Recent Activity</h2>

        <div className='overflow-x-auto'>
          <table  className='w-full'>
            <thead className='text-slate-400 border-b border-slate-700'>
              <tr>
                <th className='text-left p-3'>Feature</th>
                <th className='text-left p-3'>Model</th>
                <th className='text-left p-3'>Tokens</th>
                <th className='text-left p-3'>Cost</th>
                <th className='text-left p-3'>Latency</th>
              </tr>
            </thead>

            <tbody>
              {events.map((event) => (
                <tr key={event.id} className='border-b border-slate-800'>
                  <td className='p-3'>{event.feature}</td>
                  <td className='p-3'>{event.model}</td>
                  <td className='p-3'>{event.total_tokens}</td>
                  <td className='p-3'>{event.estimated_cost}</td>
                  <td className='p-3'>{event.latency_ms}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>      

    </main>
  )
}
