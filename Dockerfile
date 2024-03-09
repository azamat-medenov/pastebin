# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.12.0
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1

RUN apt-get update && \
    apt-get install -y gcc

RUN mkdir app

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/


RUN pip3 install poetry==$POETRY_VERSION
RUN poetry config virtualenvs.create false
RUN poetry install --only main

COPY . .
