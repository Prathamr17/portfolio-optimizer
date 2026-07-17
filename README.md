<div align="center">

# Portfolio Optimizer

**A full-stack implementation of Modern Portfolio Theory** — Efficient Frontier construction, and risk-adjusted portfolio optimization, served through a FastAPI backend and a React dashboard.

[![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://portfolio-optimizer-orpin.vercel.app)
[![API Reference](https://img.shields.io/badge/API_Reference-Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](https://portfolio-optimizer-sg9r.onrender.com/docs)

<br>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.26-013243?logo=numpy&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?logo=tailwindcss&logoColor=white)
![Deployed](https://img.shields.io/badge/Deployed-Render_%2B_Vercel-46E3B7?logo=render&logoColor=white)

</div>

<br>

> **Note:** The backend runs on Render's free tier, which spins down after 15 minutes of inactivity. The first request after idle time may take 30–50 seconds to respond. Subsequent requests are fast.

---

## Overview

Given 2–5 assets and their historical returns, the application:

1. Runs a Monte Carlo simulation across 10,000 randomly weighted portfolios
2. Constructs the Efficient Frontier — the set of portfolios offering the best return for each level of risk
3. Identifies the portfolio maximizing the Sharpe Ratio
4. Computes six risk metrics: Expected Return, Volatility, Sharpe Ratio, Sortino Ratio, Max Drawdown, and Calmar Ratio
5. Renders the allocation, metrics, and frontier as an interactive dashboard

---

## Risk Metrics

| Metric | Description |
|---|---|
| **Expected Return** | Annualized return of the optimal portfolio |
| **Volatility** | Annualized standard deviation of returns |
| **Sharpe Ratio** | Return earned per unit of total risk |
| **Sortino Ratio** | Return earned per unit of downside risk only |
| **Max Drawdown** | Largest peak-to-trough decline over the period |
| **Calmar Ratio** | Return relative to worst-case drawdown |

---

## Architecture

```
User selects assets
        │
        ▼
React frontend  ──POST /optimize──▶  FastAPI backend
                                            │
                                            ▼
                          NumPy-vectorized Monte Carlo simulation
                                  (10,000 portfolios)
                                            │
                                            ▼
                          Max-Sharpe portfolio + risk metrics
                                            │
                                            ▼
                          JSON response ──▶  Recharts dashboard
```

---

## Tech Stack

| Layer | Tools |
|---|---|
| Backend | FastAPI, NumPy, Pandas |
| Frontend | React, TypeScript, Tailwind CSS, Recharts |
| Data | yfinance (historical price data) |
| Deployment | Render (backend), Vercel (frontend) |

---

<details>
<summary><b>Project Structure</b></summary>

```
portfolio-optimizer/
├── backend/
│   └── app/
│       ├── main.py          # FastAPI app + /optimize endpoint
│       ├── models.py        # Pydantic request/response schemas
│       ├── optimizer.py     # Monte Carlo simulation + Efficient Frontier
│       ├── metrics.py       # Sharpe, Sortino, Max Drawdown, Calmar
│       └── fetch_data.py    # Historical returns via yfinance
│
└── frontend/
    └── src/
        ├── components/
        │   ├── AssetForm.tsx
        │   ├── ResultsPanel.tsx
        │   └── EfficientFrontierChart.tsx
        ├── types/portfolio.ts
        └── api/optimizer.ts
```

</details>

<details>
<summary><b>Running Locally</b></summary>

**Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API: `http://localhost:8000` · Docs: `http://localhost:8000/docs`

**Frontend**
```bash
cd frontend
npm install
npm run dev
```
Dashboard: `http://localhost:5173`

</details>

---

## Key Concepts Implemented

- **Modern Portfolio Theory** (Markowitz mean-variance optimization)
- **Monte Carlo simulation**, vectorized with NumPy for production-grade performance
- **Sharpe, Sortino, and Calmar ratios** as complementary measures of risk-adjusted return
- **Maximum drawdown** computed via cumulative return tracking
- **End-to-end type safety** — Pydantic models on the backend mirrored by TypeScript interfaces on the frontend, so schema changes surface as compile-time errors rather than runtime bugs

---

## Design Decision: Monte Carlo vs. Convex Optimization

A production quant desk would typically solve for the max-Sharpe portfolio directly using a convex optimizer such as `scipy.optimize` (SLSQP). This project instead uses random search — 10,000 simulated portfolios drawn from a Dirichlet distribution — for two reasons: it is easier to reason about and visualize, and it produces the Efficient Frontier scatter plot as a direct byproduct of the same computation used to find the optimum.

The tradeoff is that Monte Carlo search yields an approximation rather than a guaranteed global optimum. A natural extension of this project would be to add an exact solver alongside the simulation for comparison.

---

<div align="center">

*Built end-to-end — from portfolio theory to production deployment.*

</div>
