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
    """
    Generates n_portfolios random weight combinations, computes their
    (return, volatility, sharpe) triples.

    Returns:
        results: (3, n_portfolios) array -> [returns, volatility, sharpe]
        weights_record: (n_portfolios, n_assets) array of weights used
    """
    n_assets = len(mean_returns)
    results = np.zeros((3, n_portfolios))
    weights_record = np.zeros((n_portfolios, n_assets))

    for i in range(n_portfolios):
        # Dirichlet distribution ensures weights sum to 1 and are non-negative
        # (no short-selling) — standard simplifying assumption for retail-style MPT demos
        weights = np.random.dirichlet(np.ones(n_assets))
        weights_record[i] = weights

        port_return, port_vol = portfolio_performance(
            weights, mean_returns, cov_matrix, periods_per_year
        )
        sharpe = (port_return - risk_free_rate) / port_vol if port_vol > 0 else 0

        results[0, i] = port_return
        results[1, i] = port_vol
        results[2, i] = sharpe

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