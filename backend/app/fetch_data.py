"""
Fetches historical daily returns for given tickers using yfinance,
and prints/saves a ready-to-use JSON body for the /optimize endpoint.
"""

import yfinance as yf
import json
import sys
from datetime import datetime, timedelta


def fetch_returns(tickers: list[str], period_days: int = 252) -> dict:
    """
    Fetches ~1 year of daily close prices and converts to daily returns.
    period_days=252 ~= 1 trading year (standard convention, not calendar days).
    """
    end_date = datetime.today()
    # Pad calendar days since markets are closed ~30% of the time (weekends/holidays)
    start_date = end_date - timedelta(days=int(period_days * 1.6))

    print(f"Fetching {tickers} from {start_date.date()} to {end_date.date()}...")

    data = yf.download(
        tickers,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d"),
        progress=False,
    )["Close"]

    # Single ticker returns a Series, not DataFrame — normalize to DataFrame
    if len(tickers) == 1:
        data = data.to_frame(name=tickers[0])

    # Daily % returns: (price_t - price_t-1) / price_t-1
    returns = data.pct_change().dropna()

    if returns.empty:
        raise ValueError("No data returned — check ticker symbols and date range.")

    assets = []
    for ticker in tickers:
        if ticker not in returns.columns:
            print(f"WARNING: {ticker} missing from results, skipping.")
            continue
        assets.append({
            "name": ticker,
            "historical_returns": [round(float(r), 6) for r in returns[ticker].tolist()]
        })

    return {"assets": assets, "risk_free_rate": 0.04}


if __name__ == "__main__":
    # Usage: python fetch_data.py AAPL GOOGL MSFT
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ["AAPL", "GOOGL", "MSFT"]

    if not (2 <= len(tickers) <= 5):
        print("ERROR: Provide 2-5 tickers (your API requires this range).")
        sys.exit(1)

    payload = fetch_returns(tickers)

    with open("sample_request.json", "w") as f:
        json.dump(payload, f, indent=2)

    print(f"\nSaved {len(payload['assets'])} assets to sample_request.json")
    print(f"Each asset has {len(payload['assets'][0]['historical_returns'])} daily returns")
    print("\nTest it with:")
    print("curl -X POST http://localhost:8000/optimize -H 'Content-Type: application/json' -d @sample_request.json")