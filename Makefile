# Makefile for awesome-playground
# https://makefiletutorial.com/

.PHONY: lint fix format test run clean install help

# Default target
.DEFAULT_GOAL := help

## lint: Run linters (ruff check, ruff format, mypy)
lint:
	@echo "🔍 Running linters..."
	uv run ruff check . && \
	uv run ruff format . --check && \
	uv run mypy .
	@echo "✅ Linting complete!"

## fix: Run Fix with linters (ruff check, ruff format, mypy)
fix:
	@echo "🔍 Running Fix with linters..."
	uv run ruff check . --fix && \
	uv run ruff format .
	@echo "✅ Fixing complete!"

## format: Format code with ruff
format:
	@echo "🎨 Formatting code..."
	uv run ruff format .
	@echo "✅ Formatting complete!"

## test: Run tests with pytest
test:
	@echo "🧪 Running tests..."
	uv run pytest
	@echo "✅ Tests complete!"

## run: Run the FastAPI service
run:
	@echo "🚀 Starting Awesome Service..."
	uv run uvicorn awesome_playground.awesome_service:app --reload

## clean: Remove cache and build artifacts
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean complete!"

## install: Install dependencies with uv
install:
	@echo "📦 Installing dependencies..."
	uv sync
	@echo "✅ Installation complete!"

## help: Show this help message
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## /  /'
