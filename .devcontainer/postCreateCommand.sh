#!/usr/bin/env bash
# /workspase is inaccessible on image creation it is mounted after that
# here are modification on mounted volume with project

poetry check
poetry install --no-interaction --no-cache --no-root

sudo chown -R nonroot /workspace
