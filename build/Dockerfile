# For more information, please refer to https://aka.ms/vscode-docker-python
# -------------------------- base ------------------------------------------
FROM python:3.12-slim as base

RUN apt-get update && apt-get upgrade -y

ENV POETRY_VENV=/opt/poetry-venv
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# -------------------------- dev -------------------------------------------
FROM base as dev
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get -y install git

# -------------------------- prod ------------------------------------------
FROM base as prod

WORKDIR /app
COPY .. .

RUN poetry check
RUN poetry install --no-interaction --no-cache --no-root

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["poetry", "run", "python", "-m", "src"]
