# For more information, please refer to https://aka.ms/vscode-docker-python
# -------------------------- base ------------------------------------------
FROM python:3.12-slim as base

RUN apt-get update && apt-get upgrade -y

# poetry install
ENV POETRY_VENV=/opt/poetry-venv
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# create non root user
ARG USER_NAME=nonroot
ARG USER_ID=5678
RUN groupadd --gid $USER_ID $USER_NAME \
    && useradd --uid $USER_ID --gid $USER_ID -m $USER_NAME

# -------------------------- dev -------------------------------------------
FROM base as dev
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get install -y git && \
    apt-get install -y gnupg2 && \
    apt-get install -y shfmt && \
    apt-get install -y make && \
    # bsdmainutils for hexdump
    apt-get install -y bsdmainutils && \
    # netcat for nc
    apt-get install -y netcat-traditional && \
    apt-get install -y curl

# [Optional] Add sudo support.
RUN apt-get install -y sudo \
    && echo $USER_NAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USER_NAME \
    && chmod 0440 /etc/sudoers.d/$USER_NAME
USER $USER_NAME

# -------------------------- prod ------------------------------------------
FROM base as prod

WORKDIR /app
COPY .. .

RUN poetry check
RUN poetry install --no-interaction --no-cache --no-root

# Adds permission to access the /app folder
RUN chown -R $USER_NAME /app
USER $USER_NAME

CMD ["poetry", "run", "python", "-m", "src"]
