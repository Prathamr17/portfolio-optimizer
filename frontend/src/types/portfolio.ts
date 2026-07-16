export interface Asset {
  name: string;
  historical_returns: number[];
}

export interface OptimizeRequest {
  assets: Asset[];
  risk_free_rate: number;
}

export interface RiskMetrics {
  expected_return: number;
  volatility: number;
  sharpe_ratio: number;
  sortino_ratio: number;
  max_drawdown: number;
  calmar_ratio: number;
}

export interface FrontierPoint {
  return: number;
  volatility: number;
}

export interface OptimizeResponse {
  asset_names: string[];
  optimal_weights: number[];
  metrics: RiskMetrics;
  efficient_frontier_points: FrontierPoint[];
}