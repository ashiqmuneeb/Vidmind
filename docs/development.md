# VidMind Developer & Contributor Guide

## 1. Monorepo Structure

```
vidmind/
├── backend/app/        # FastAPI Application, Services, Repositories, Workers
├── frontend/           # Vite + React + TypeScript + Tailwind UI
├── data/               # Local cache, sqlite database, audio and frame files
├── docs/               # Architecture and operational documentation
├── scripts/            # CLI utilities and environment setup scripts
└── tests/              # Multi-tier test suite (unit, integration, golden)
```

## 2. Running Test Suites

```powershell
# Run backend unit and integration tests
pytest backend/tests/ -v

# Run golden accuracy evaluations
pytest backend/tests/evaluation/ -v
```

## 3. Code Style & Standards
- Python: Formatted with Ruff/Black; Type checked with Mypy; Strict Pydantic v2 schemas.
- Frontend: TypeScript strict mode; ESLint; Tailwind utility classes; semantic accessible HTML.
