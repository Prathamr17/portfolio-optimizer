# Portfolio Optimizer

A full-stack application that computes optimal asset allocations using Modern Portfolio Theory (Markowitz mean-variance optimization).

**Live demo:** [vercel-url-here]

## What it does

Given 2-5 assets and their historical returns, the app:
1. Runs a Monte Carlo simulation (10,000 random portfolios) to build the Efficient Frontier
2. Identifies the portfolio with the maximum Sharpe Ratio (best risk-adjusted return)
3. Computes 6 risk metrics: Expected Return, Volatility, Sharpe Ratio, Sortino Ratio, Max Drawdown, Calmar Ratio
4. Visualizes the frontier and optimal allocation in an interactive dashboard

## Tech Stack

- **Backend:** FastAPI, NumPy, Pandas
- **Frontend:** React, TypeScript, Tailwind CSS, Recharts
- **Data:** yfinance (historical price data)
- **Deployment:** Railway (backend), Vercel (frontend)

---

## Backend : 

#### Structure :

```
portfolio-optimizer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app + endpoints
│   │   ├── models.py            # Pydantic request/response schemas
│   │   ├── optimizer.py         # Core MPT optimization logic
│   │   ├── metrics.py           # Risk metric calculations
│   │   └── database.py          # SQLite persistence (optional)
│   ├── tests/
│   │   └── test_optimizer.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
```

#### Run commands - 
```cmd
  cd backend
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload
```
---
## Frontend : 

#### Structure : 


```
portfolio-optimizer/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AssetForm.tsx
│   │   │   ├── ResultsPanel.tsx
│   │   │   ├── EfficientFrontierChart.tsx
│   │   │   └── WeightsChart.tsx
│   │   ├── types/
│   │   │   └── portfolio.ts
│   │   ├── api/
│   │   │   └── optimizer.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── vite.config.ts
```
#### Run commands -
```cmd
  cd frontend
  npm install
  npm run dev
```

---
## Key concepts implemented

- Modern Portfolio Theory (Markowitz mean-variance optimization)
- Monte Carlo simulation for Efficient Frontier generation
- Sharpe, Sortino, and Calmar ratios for risk-adjusted performance
- Maximum drawdown calculation via cumulative return tracking