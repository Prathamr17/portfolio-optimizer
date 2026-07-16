# portfolio-optimizer
Finance Portfolio Optimizer

---

## Backend : 

#### Structure :

```
portfolio-optimizer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app + endpoints
│   │   ├── models.py            # Pydantic request/response schemas
│   │   ├── optimizer.py         # Core MPT optimization logic
│   │   ├── metrics.py           # Risk metric calculations
│   │   └── database.py          # SQLite persistence (optional)
│   ├── tests/
│   │   └── test_optimizer.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
```

#### Run commands - 
```cmd
  cd backend
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload
```
---
## Frontend : 

#### Structure : 


```
portfolio-optimizer/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AssetForm.tsx
│   │   │   ├── ResultsPanel.tsx
│   │   │   ├── EfficientFrontierChart.tsx
│   │   │   └── WeightsChart.tsx
│   │   ├── types/
│   │   │   └── portfolio.ts
│   │   ├── api/
│   │   │   └── optimizer.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── vite.config.ts
```
#### Run commands -
```cmd
  cd frontend
  npm install
  npm run dev
```
