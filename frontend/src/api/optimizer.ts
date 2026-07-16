import axios from "axios";
import type { OptimizeRequest, OptimizeResponse } from "../types/portfolio";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function optimizePortfolio(
  request: OptimizeRequest
): Promise<OptimizeResponse> {
  const response = await axios.post<OptimizeResponse>(
    `${API_BASE_URL}/optimize`,
    request
  );
  return response.data;
}