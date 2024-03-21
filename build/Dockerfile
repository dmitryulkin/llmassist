# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim as base
RUN apt-get update && apt-get upgrade -y

FROM base as dev
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# To avoid poetry installatin each time
FROM base as poetry

ENV POETRY_VENV=/opt/poetry-venv

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry

FROM poetry as prod

COPY --from=poetry ${POETRY_VENV} ${POETRY_VENV}
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app
COPY .. .

RUN poetry check
RUN poetry install --no-interaction --no-cache --no-root

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["poetry", "run", "python", "-m", "src"]
