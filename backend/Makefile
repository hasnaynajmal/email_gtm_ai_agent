# Scripts for development and deployment

# Run development server
start:
	python run.py

# Run with uvicorn directly
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Initialize database
init-db:
	python -m app.db.init_db

# Format code with black
format:
	black app/

# Lint code
lint:
	pylint app/

# Run tests
test:
	pytest

# Docker commands
docker-build:
	docker build -t fastapi-template .

docker-run:
	docker run -p 8000:8000 --env-file .env fastapi-template

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

docker-compose-logs:
	docker-compose logs -f

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

.PHONY: start dev init-db format lint test docker-build docker-run docker-compose-up docker-compose-down docker-compose-logs clean
