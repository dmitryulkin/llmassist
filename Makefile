.PHONY: run test coverage
run:
	poetry run python -m src
# pytest
test:
	poetry run pytest --cov=src
coverage:
	poetry run pytest --cov=src --cov-report=html
# alembic migrations
.PHONY: dbgen dbup
dbgen:
	poetry run alembic revision --autogenerate -m "${NAME}"
dbup:
	poetry run alembic upgrade head
