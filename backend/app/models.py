from pydantic import BaseModel, Field
from typing import List


class AssetInput(BaseModel):
    name: str
    # Historical daily/monthly returns as a list of decimals (e.g., 0.02 = 2%)
    historical_returns: List[float] = Field(..., min_length=10)


class OptimizeRequest(BaseModel):
    assets: List[AssetInput] = Field(..., min_length=2, max_length=5)
    risk_free_rate: float = 0.04  # annualized, default 4%


class RiskMetrics(BaseModel):
    expected_return: float
    volatility: float
    sharpe_ratio: float
    sortino_ratio: float
    max_drawdown: float
    calmar_ratio: float


class OptimizeResponse(BaseModel):
    asset_names: List[str]
    optimal_weights: List[float]
    metrics: RiskMetrics
    efficient_frontier_points: List[dict]  # for plotting on frontend