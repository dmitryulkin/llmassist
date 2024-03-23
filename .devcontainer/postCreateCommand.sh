#!/usr/bin/env bash
# Motivation: /workspase is inaccessible on image creation bacuse of it is
# mounted after that. Here are modifications on mounted volume with sources
poetry check
poetry install --with dev --no-interaction --no-cache --no-root

sudo chown -R nonroot /workspace
