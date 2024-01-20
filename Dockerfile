# Build stage
FROM python:alpine AS build

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache mariadb-connector-c-dev build-base libffi-dev openssl-dev bash && \
    pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:alpine

WORKDIR /app

COPY --from=build /usr/local /usr/local
COPY . .

# Install bash in the runtime stage
RUN apk add --no-cache bash

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
