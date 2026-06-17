.PHONY: install test lint format clean run-api run-ui

install:
	pip install -e .[all]
	pip install black isort flake8 mypy pre-commit
	pre-commit install

test:
	pytest tests/

lint:
	flake8 src/ tests/
	mypy src/
	black --check src/ tests/
	isort --check-only src/ tests/

format:
	black src/ tests/
	isort src/ tests/

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +

run-api:
	uvicorn ai_distiller.api.server:app --reload --host 0.0.0.0 --port 8000

run-ui:
	python src/ai_distiller/ui/app.py
