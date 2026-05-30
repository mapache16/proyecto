.PHONY: help setup run test clean docker-build docker-up docker-down

help:
	@echo "AMCO - Centro Inteligente Metropolitano"
	@echo "======================================="
	@echo "Available commands:"
	@echo "  make setup       - Setup initial environment"
	@echo "  make run         - Run all services"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean cache and temp files"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up   - Start Docker services"
	@echo "  make docker-down - Stop Docker services"

setup:
	@echo "Setting up environment..."
	@python -m venv venv
	@. venv/bin/activate && pip install -r requirements.txt
	@mkdir -p backend/app/ml/models logs tests
	@cp .env.example .env
	@python seed.py

run:
	@echo "Starting AMCO services..."
	@echo "Terminal 1: IoT Simulator"
	@python iot_simulator.py & \
	echo "Terminal 2: API Backend" && \
	python api.py & \
	echo "Terminal 3: Dashboard" && \
	streamlit run dashboard_avanzado.py

test:
	@echo "Running tests..."
	@pytest tests/ -v --cov=backend/app

clean:
	@echo "Cleaning..."
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name '*.pyc' -delete
	@rm -rf .pytest_cache .coverage htmlcov

docker-build:
	@echo "Building Docker images..."
	@docker-compose build

docker-up:
	@echo "Starting Docker services..."
	@docker-compose up -d

docker-down:
	@echo "Stopping Docker services..."
	@docker-compose down
