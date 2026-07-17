import numpy as np
from typing import List, Tuple


def compute_returns_matrix(assets_returns: List[List[float]]) -> np.ndarray:
    """Stack asset return series into a (n_periods, n_assets) matrix.
    Assumes all series are pre-aligned and equal length (validated in main.py)."""
    return np.array(assets_returns).T


def annualize_return(mean_period_return: float, periods_per_year: int = 252) -> float:
    return (1 + mean_period_return) ** periods_per_year - 1


def annualize_volatility(period_std: float, periods_per_year: int = 252) -> float:
    return period_std * np.sqrt(periods_per_year)


def portfolio_performance(
    weights: np.ndarray,
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    periods_per_year: int = 252,
) -> Tuple[float, float]:
    """Returns (annualized_return, annualized_volatility) for given weights."""
    port_period_return = np.dot(weights, mean_returns)
    port_period_var = np.dot(weights.T, np.dot(cov_matrix, weights))
    port_annual_return = annualize_return(port_period_return, periods_per_year)
    port_annual_vol = annualize_volatility(np.sqrt(port_period_var), periods_per_year)
    return port_annual_return, port_annual_vol


def monte_carlo_simulation(
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float,
    n_portfolios: int = 10000,
    periods_per_year: int = 252,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    n_assets = len(mean_returns)

    # Generate all random weights at once (vectorized) instead of looping
    weights_record = np.random.dirichlet(np.ones(n_assets), size=n_portfolios)

    # Vectorized portfolio returns: (n_portfolios, n_assets) @ (n_assets,) -> (n_portfolios,)
    port_period_returns = weights_record @ mean_returns
    port_annual_returns = annualize_return(port_period_returns, periods_per_year)

    # Vectorized portfolio variance for all portfolios at once
    port_variances = np.einsum('ij,jk,ik->i', weights_record, cov_matrix, weights_record)
    port_annual_vols = annualize_volatility(np.sqrt(port_variances), periods_per_year)

    sharpe = np.where(
        port_annual_vols > 0,
        (port_annual_returns - risk_free_rate) / port_annual_vols,
        0
    )

    results = np.array([port_annual_returns, port_annual_vols, sharpe])
    return results, weights_record


def find_optimal_portfolio(
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float,
    n_portfolios: int = 10000,
    periods_per_year: int = 252,
) -> dict:
    """Runs Monte Carlo sim, finds max-Sharpe portfolio, and returns
    both the optimal weights and the full frontier for plotting."""
    results, weights_record = monte_carlo_simulation(
        mean_returns, cov_matrix, risk_free_rate, n_portfolios, periods_per_year
    )

    max_sharpe_idx = np.argmax(results[2])
    optimal_weights = weights_record[max_sharpe_idx]
    optimal_return = results[0, max_sharpe_idx]
    optimal_vol = results[1, max_sharpe_idx]
    optimal_sharpe = results[2, max_sharpe_idx]

    # Downsample frontier points for frontend plotting (don't send all 10k)
    sample_idx = np.random.choice(n_portfolios, size=min(500, n_portfolios), replace=False)
    frontier_points = [
        {"return": float(results[0, i]), "volatility": float(results[1, i])}
        for i in sample_idx
    ]

    return {
        "weights": optimal_weights,
        "return": optimal_return,
        "volatility": optimal_vol,
        "sharpe": optimal_sharpe,
        "frontier_points": frontier_points,
    }