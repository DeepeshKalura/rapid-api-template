# 🚀 RapidAPI Template (FastAPI)

High-performance, production-ready template for building and deploying APIs to RapidAPI using Python 3.12, FastAPI, and UV.

## 🛠 Features

- **FastAPI:** Modern web framework with automatic OpenAPI documentation
- **UV Dependency Management:** 10x faster than pip
- **Auto-Spec Generation:** Pre-commit hooks create `openapi.json` and `openapi.yaml` on commit
- **RapidAPI Ready:** Scripts to extract tests for RapidAPI Studio
- **CI/CD:** GitHub Actions validate API and tests
- **Docker Support:** Ready-to-use Dockerfiles for deployment

## 📁 Structure

```
├── app/               # FastAPI application
│   └── main.py       # Add your API endpoints here
├── tests/            # Tests
├── scripts/          # Utility scripts (OpenAPI generation, test extraction)
├── .github/          # GitHub Actions workflows
├── pyproject.toml    # Dependencies and config
├── Dockerfile        # Dev container
└── Dockerfile.prod   # Prod container
```

## 🚀 Quick Start

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup
uv sync
cp .env.example .env

# Run
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API available at http://localhost:8000/docs

## 📦 Generate OpenAPI

```bash
# Auto-generates on commit, or run manually:
pre-commit run --all-files
```

Creates `openapi.json`, `openapi.yaml`, `.rapidapi/tests/`

## 🐳 Docker

```bash
# Dev
docker build -t api-dev .
docker run -p 8000:8000 api-dev

# Prod  
docker build -f Dockerfile.prod -t api-prod .
docker run -p 8000:8000 api-prod
```

## 🚢 Deploy to RapidAPI

1. `pre-commit run --all-files`
2. Upload `openapi.yaml` to RapidAPI Dashboard
3. Use `.rapidapi/tests/` for RapidAPI Studio tests
4. `bash scripts/setup-rapidapi-secrets.sh` for CI/CD

## 🧪 Tests

```bash
uv run pytest tests/ -v
```

## 📝 Getting Started

Edit `app/main.py` to add your API endpoints. The template includes:
- `/ping` - Health check
- `/` - Root endpoint

Add more endpoints as needed. All changes auto-generate OpenAPI spec on commit.
