# For more information, please refer to https://aka.ms/vscode-docker-python
# -------------------------- base ------------------------------------------
FROM python:3.12-slim as base

RUN apt-get update && apt-get upgrade -y

ENV POETRY_VENV=/opt/poetry-venv
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# create non root user
ARG USERNAME=nonroot
ARG USER_UID=5678
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# -------------------------- dev -------------------------------------------
FROM base as dev
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get install -y git

# [Optional] Add sudo support.
RUN apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME

# -------------------------- prod ------------------------------------------
FROM base as prod

WORKDIR /app
COPY .. .

RUN poetry check
RUN poetry install --no-interaction --no-cache --no-root

# Adds permission to access the /app folder
RUN chown -R $USERNAME /app
USER $USERNAME

CMD ["poetry", "run", "python", "-m", "src"]
