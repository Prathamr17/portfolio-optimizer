import type { OptimizeResponse } from "../types/portfolio";

interface ResultsPanelProps {
  results: OptimizeResponse;
}

const METRIC_LABELS: Record<string, string> = {
  expected_return: "Expected Return",
  volatility: "Volatility",
  sharpe_ratio: "Sharpe Ratio",
  sortino_ratio: "Sortino Ratio",
  max_drawdown: "Max Drawdown",
  calmar_ratio: "Calmar Ratio",
};

const isPercentMetric = (key: string) =>
  ["expected_return", "volatility", "max_drawdown"].includes(key);

export default function ResultsPanel({ results }: ResultsPanelProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Optimal Allocation
        </h3>
        <div className="space-y-2">
          {results.asset_names.map((name, i) => (
            <div key={name} className="flex items-center gap-3">
              <span className="w-16 text-sm font-medium text-gray-700">
                {name}
              </span>
              <div className="flex-1 bg-gray-100 rounded-full h-6 overflow-hidden">
                <div
                  className="bg-blue-600 h-full flex items-center justify-end pr-2"
                  style={{ width: `${results.optimal_weights[i] * 100}%` }}
                >
                  <span className="text-xs text-white font-medium">
                    {(results.optimal_weights[i] * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Risk Metrics
        </h3>
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(results.metrics).map(([key, value]) => (
            <div key={key} className="bg-gray-50 p-3 rounded-lg">
              <p className="text-xs text-gray-500">{METRIC_LABELS[key]}</p>
              <p className="text-xl font-semibold text-gray-900">
                {isPercentMetric(key)
                  ? `${(value * 100).toFixed(2)}%`
                  : value.toFixed(2)}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}