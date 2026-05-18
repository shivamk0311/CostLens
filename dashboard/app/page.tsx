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
}

type ModelCost = {
  model: string;
  total_cost_usd: number;
}

export default function Home(){

  const [summary, setSummary] = useState<CostSummary | null>(null);
  const [featureCosts, setFeatureCosts] = useState<FeatureCost[]>([]);
  const [modelCosts, setModelCosts] = useState<ModelCost[]>([]);

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

          <div className='col-span-1 md:col-span-2 mt-10 rounded-xl bg-slate-900 p-6'>
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
          <div className='col-span-1 md:col-span-2 mt-10 rounded-xl bg-slate-900 p-6'>
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
      )}

    </main>
  )
}
