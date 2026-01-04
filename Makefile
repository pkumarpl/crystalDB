.PHONY: help install dev-install clean test lint format docker-build docker-up docker-down init-db import-data

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -e .

dev-install:  ## Install development dependencies
	pip install -e ".[dev]"
	pre-commit install

clean:  ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf dist/ build/ htmlcov/ .coverage

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=src/crystaldb --cov-report=html --cov-report=term

lint:  ## Run linters
	ruff check src/ tests/
	mypy src/

format:  ## Format code
	black src/ tests/
	ruff check --fix src/ tests/

run:  ## Run development server
	python -m crystaldb.main

run-reload:  ## Run development server with auto-reload
	uvicorn crystaldb.main:app --reload --host 0.0.0.0 --port 8000

docker-build:  ## Build Docker image
	docker-compose build

docker-up:  ## Start Docker services
	docker-compose up -d

docker-down:  ## Stop Docker services
	docker-compose down

docker-logs:  ## View Docker logs
	docker-compose logs -f

init-db:  ## Initialize database (create tables)
	python scripts/init_db.py

import-data:  ## Import data from CSV files
	python scripts/import_data.py

db-shell:  ## Open MySQL shell
	docker-compose exec db mysql -u crystaldb_user -p crystaldb

api-shell:  ## Open shell in API container
	docker-compose exec api /bin/bash

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files
