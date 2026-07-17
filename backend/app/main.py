from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

from app.models import OptimizeRequest, OptimizeResponse, RiskMetrics
from app.optimizer import compute_returns_matrix, find_optimal_portfolio
from app.metrics import compute_all_metrics

app = FastAPI(title="Portfolio Optimizer API", version="1.0.0")

# CORS — needed for Vercel frontend to call Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # local dev
        "https://portfolio-optimizer-orpin.vercel.app",  # production frontend
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "portfolio-optimizer-api"}


@app.post("/optimize", response_model=OptimizeResponse)
def optimize_portfolio(request: OptimizeRequest):
    asset_names = [a.name for a in request.assets]
    returns_lists = [a.historical_returns for a in request.assets]

    # Validate equal-length return series (required for a valid covariance matrix)
    lengths = {len(r) for r in returns_lists}
    if len(lengths) > 1:
        raise HTTPException(
            status_code=400,
            detail="All assets must have historical_returns of the same length.",
        )

    returns_matrix = compute_returns_matrix(returns_lists)  # (n_periods, n_assets)
    mean_returns = np.mean(returns_matrix, axis=0)
    cov_matrix = np.cov(returns_matrix.T)

    result = find_optimal_portfolio(
        mean_returns=mean_returns,
        cov_matrix=cov_matrix,
        risk_free_rate=request.risk_free_rate,
    )

    metrics = compute_all_metrics(
        period_returns=returns_matrix,
        weights=result["weights"],
        annual_return=result["return"],
        annual_vol=result["volatility"],
        risk_free_rate=request.risk_free_rate,
    )

    return OptimizeResponse(
        asset_names=asset_names,
        optimal_weights=[round(float(w), 4) for w in result["weights"]],
        metrics=RiskMetrics(**metrics),
        efficient_frontier_points=result["frontier_points"],
    )