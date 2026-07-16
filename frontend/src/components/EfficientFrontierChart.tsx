import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { FrontierPoint } from "../types/portfolio";

interface EfficientFrontierChartProps {
  points: FrontierPoint[];
  optimalPoint: { return: number; volatility: number };
}

export default function EfficientFrontierChart({
  points,
  optimalPoint,
}: EfficientFrontierChartProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold text-gray-900 mb-3">
        Efficient Frontier
      </h3>
      <ResponsiveContainer width="100%" height={350}>
        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            type="number"
            dataKey="volatility"
            name="Volatility"
            tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
            label={{ value: "Volatility (Risk)", position: "bottom" }}
          />
          <YAxis
            type="number"
            dataKey="return"
            name="Return"
            tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
            label={{ value: "Expected Return", angle: -90, position: "left" }}
          />
          <Tooltip
            formatter={(value) => {
              const numericValue = typeof value === "number" ? value : Number(value ?? 0);
              return `${(numericValue * 100).toFixed(2)}%`;
            }}
          />
          <Scatter data={points} fill="#93c5fd" opacity={0.6} />
          <Scatter
            data={[optimalPoint]}
            fill="#dc2626"
            shape="star"
          />
        </ScatterChart>
      </ResponsiveContainer>
      <p className="text-xs text-gray-500 mt-2">
        Blue dots = simulated portfolios. Red star = optimal (max Sharpe) portfolio.
      </p>
    </div>
  );
}