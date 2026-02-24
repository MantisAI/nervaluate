.PHONY: help all test test-fast lint format typecheck check clean install-dev

help:
	@echo "Targets:"
	@echo "  all          Run full check: format, typecheck, test (default)"
	@echo "  install-dev  Install package with dev dependencies (uv sync --extra dev)"
	@echo "  test         Run tests with coverage"
	@echo "  test-fast    Run tests without coverage"
	@echo "  lint         Run black (check only), pylint, mypy"
	@echo "  format       Run black to fix formatting"
	@echo "  typecheck    Run mypy"
	@echo "  check        Run format, typecheck, and test (CI-style)"
	@echo "  clean        Remove caches and build artifacts"

all: check

install-dev:
	uv sync --extra dev

test:
	uv run pytest --cov=nervaluate --cov-report=term-missing -v

test-fast:
	uv run pytest -v

lint:
	uv run black --check src tests
	uv run pylint src tests
	uv run mypy src

format:
	uv run black src tests

typecheck:
	uv run mypy src

check: format lint typecheck test clean

clean:
	rm -rf .coverage .mypy_cache .pytest_cache
	rm -rf dist build *.egg-info src/*.egg-info
