.PHONY: run test coverage
run:
	poetry run python -m src

test:
	poetry run pytest --cov=src

coverage:
	poetry run pytest --cov=src --cov-report=html
