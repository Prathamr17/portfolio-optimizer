import numpy as np
from typing import List


def sortino_ratio(
    period_returns: np.ndarray,
    weights: np.ndarray,
    risk_free_rate: float,
    periods_per_year: int = 252,
) -> float:
    """Like Sharpe, but only penalizes downside volatility (negative returns).
    This is what makes Sortino more forgiving of upside swings."""
    port_returns = period_returns @ weights  # (n_periods,) portfolio return series
    port_annual_return = annualize_return(np.mean(port_returns), periods_per_year)

    downside_returns = port_returns[port_returns < 0]
    if len(downside_returns) == 0:
        return float("inf")  # no downside risk observed — cap this on the frontend

    downside_std = np.std(downside_returns)
    downside_annual_std = downside_std * np.sqrt(periods_per_year)

    if downside_annual_std == 0:
        return float("inf")

    return (port_annual_return - risk_free_rate) / downside_annual_std


def max_drawdown(period_returns: np.ndarray, weights: np.ndarray) -> float:
    """Largest peak-to-trough decline in cumulative portfolio value."""
    port_returns = period_returns @ weights
    cumulative = np.cumprod(1 + port_returns)
    running_max = np.maximum.accumulate(cumulative)
    drawdowns = (cumulative - running_max) / running_max
    return float(np.min(drawdowns))  # negative number, e.g., -0.23 = -23%


def calmar_ratio(
    annual_return: float,
    max_dd: float,
) -> float:
    """Return per unit of worst-case drawdown risk. Higher = better."""
    if max_dd == 0:
        return float("inf")
    return annual_return / abs(max_dd)


def annualize_return(mean_period_return: float, periods_per_year: int = 252) -> float:
    return (1 + mean_period_return) ** periods_per_year - 1


def compute_all_metrics(
    period_returns: np.ndarray,
    weights: np.ndarray,
    annual_return: float,
    annual_vol: float,
    risk_free_rate: float,
    periods_per_year: int = 252,
) -> dict:
    sharpe = (annual_return - risk_free_rate) / annual_vol if annual_vol > 0 else 0
    sortino = sortino_ratio(period_returns, weights, risk_free_rate, periods_per_year)
    mdd = max_drawdown(period_returns, weights)
    calmar = calmar_ratio(annual_return, mdd)

    return {
        "expected_return": round(annual_return, 4),
        "volatility": round(annual_vol, 4),
        "sharpe_ratio": round(sharpe, 4),
        "sortino_ratio": round(sortino, 4) if sortino != float("inf") else 999.0,
        "max_drawdown": round(mdd, 4),
        "calmar_ratio": round(calmar, 4) if calmar != float("inf") else 999.0,
    }