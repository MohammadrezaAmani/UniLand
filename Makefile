# Makefile for UniLand Bot

.PHONY: help install migrate run test clean docker-up docker-down

help:
	@echo "UniLand Bot - Available commands:"
	@echo "  make install      - Install dependencies with uv"
	@echo "  make migrate      - Run database migrations"
	@echo "  make superuser    - Create Django superuser"
	@echo "  make run-bot      - Run Telegram bot"
	@echo "  make run-web      - Run Django development server"
	@echo "  make run-celery   - Run Celery worker"
	@echo "  make run-beat     - Run Celery beat"
	@echo "  make test         - Run tests"
	@echo "  make format       - Format code with black"
	@echo "  make lint         - Lint code with ruff"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make clean        - Clean temporary files"

install:
	uv pip install -r requirements.txt

migrate:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

run-bot:
	python manage.py runbot

run-web:
	python manage.py runserver

run-celery:
	celery -A config worker -l info

run-beat:
	celery -A config beat -l info

test:
	pytest --cov=apps --cov-report=html --cov-report=term-missing

format:
	black .

lint:
	ruff check .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
