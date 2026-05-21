# CostLens

CostLens is an AI cost observability platform designed to help developers understand, monitor, and optimize Large Language Model (LLM) usage. It acts as a proxy layer between applications and LLM APIs, capturing telemetry such as token usage, latency, model usage, and estimated inference cost while providing analytics through an interactive dashboard.

The goal of CostLens is to give AI applications visibility into how models are being used, where costs are coming from, and how inference spending can be optimized.

---

## Features

### AI Request Proxy
- Intercepts OpenAI chat requests through a FastAPI proxy
- Tracks request metadata and usage patterns
- Supports feature tagging through request headers

### Cost Analytics
- Total request count
- Token usage tracking
- Average latency tracking
- Estimated inference cost calculation
- Cost breakdown by feature
- Cost breakdown by model

### Dashboard
- Built with Next.js and Tailwind CSS
- KPI cards
- Cost visualizations
- Recent activity table
- Interactive analytics UI

### Exact Prompt Cache
- SHA256-based exact prompt matching
- Stores prompt, embeddings, responses, and hit counts
- Reduces repeated API calls for identical prompts

### Containerized Architecture
- PostgreSQL database
- FastAPI backend
- Next.js dashboard
- Docker Compose setup

---

## Architecture

```text
User Request
      ↓
Next.js Dashboard
      ↓
FastAPI Proxy
      ↓
Cache Check
      ↓
OpenAI API
      ↓
Telemetry Collection
      ↓
PostgreSQL
      ↓
Analytics Dashboard
```

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- OpenAI API

### Frontend
- Next.js
- React
- Tailwind CSS
- Recharts

### Infrastructure
- Docker
- Docker Compose

---

## Project Structure

```text
CostLens/

├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── dependencies/
│
├── dashboard/
│
├── docker-compose.yml
│
└── README.md
```

---

## Local Setup

Clone repository:

```bash
git clone <your-repository-url>
cd CostLens
```

Create environment variables:

```env
OPENAI_API_KEY=your_key_here
```

Start application:

```bash
docker compose up --build
```

Application URLs:

```text
Dashboard:
http://localhost:3000

Backend:
http://localhost:8000

Swagger:
http://localhost:8000/docs
```

---

## Example Request

Endpoint:

```text
POST /v1/chat/completions
```

Header:

```text
X-CostLens-Feature: summarizer
```

Body:

```json
{
  "model":"gpt-4o-mini",
  "messages":[
    {
      "role":"user",
      "content":"Summarize ways to reduce AWS spending"
    }
  ],
  "temperature":0.5
}
```

---

## Current Progress

Completed:

- FastAPI proxy integration
- PostgreSQL event persistence
- Cost analytics APIs
- Dashboard MVP
- Dockerized services
- Exact prompt caching
- pgvector integration

In Progress:

- Embedding-based semantic cache
- Similarity search using vectors

Planned:

- Kafka event pipeline
- Cost anomaly detection
- Deployment
- Performance benchmarking
- Advanced monitoring

---

## Why CostLens?

LLM applications often become expensive without visibility into usage patterns. CostLens aims to provide an observability layer similar to how tools like Datadog provide monitoring for infrastructure, but focused specifically on AI workloads.

---

## Author

Shivam Khokhani

Computer Science Graduate — University of Texas at Arlington

Interested in AI systems, backend engineering, and developer infrastructure.
