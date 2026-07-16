# -- database.py uses this schema if you want to persist runs
# CREATE TABLE IF NOT EXISTS optimization_runs (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     asset_names TEXT NOT NULL,        -- JSON array
#     risk_free_rate REAL NOT NULL,
#     optimal_weights TEXT NOT NULL,    -- JSON array
#     expected_return REAL,
#     volatility REAL,
#     sharpe_ratio REAL,
#     sortino_ratio REAL,
#     max_drawdown REAL,
#     calmar_ratio REAL
# );