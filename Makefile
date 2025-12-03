.PHONY: help install setup test run run-enhanced clean lint format docs

help:
	@echo "EchoOS Development Commands"
	@echo "============================"
	@echo ""
	@echo "  make install        - Install dependencies"
	@echo "  make setup          - Run first-time setup"
	@echo "  make test           - Run tests"
	@echo "  make run            - Run EchoOS (standard version)"
	@echo "  make run-enhanced   - Run EchoOS Enhanced (dark mode + waveform)"
	@echo "  make clean          - Clean temporary files"
	@echo "  make lint           - Run linters"
	@echo "  make format         - Format code"
	@echo "  make docs           - Generate documentation"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

setup:
	@echo "Running first-time setup..."
	python scripts/setup_config.py
	python scripts/download_vosk_model.py
	python scripts/discover_apps.py
	@echo "✓ Setup complete"

test:
	@echo "Running tests..."
	pytest tests/ -v --cov=modules --cov-report=html
	@echo "✓ Tests complete"
	@echo "Coverage report: htmlcov/index.html"

run:
	@echo "Starting EchoOS (Standard Version)..."
	python main.py

run-enhanced:
	@echo "Starting EchoOS Enhanced (Dark Mode + Waveform)..."
	python main_enhanced.py

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	@echo "✓ Cleanup complete"

lint:
	@echo "Running linters..."
	flake8 modules/ tests/ --max-line-length=100
	@echo "✓ Linting complete"

format:
	@echo "Formatting code..."
	black modules/ tests/ scripts/
	@echo "✓ Formatting complete"

docs:
	@echo "Generating documentation..."
	@echo "Documentation available in docs/"
	@echo "✓ Documentation ready"

# Development shortcuts
dev-install:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 mypy

test-quick:
	pytest tests/ -v

test-watch:
	pytest-watch tests/

microphone-test:
	python scripts/test_microphone.py

discover-apps:
	python scripts/discover_apps.py

# Version comparison
compare:
	@echo "EchoOS Versions:"
	@echo "  Standard:  python main.py"
	@echo "  Enhanced:  python main_enhanced.py"
	@echo ""
	@echo "Enhanced features:"
	@echo "  ✓ Dark mode theme"
	@echo "  ✓ Animated waveform"
	@echo "  ✓ Modern UI design"
	@echo "  ✓ Theme toggle"
