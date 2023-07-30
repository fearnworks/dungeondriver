FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Install dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y git vim build-essential python3-dev python3-pip && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip

# Create appuser
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# Create app directory and change ownership to appuser
RUN mkdir /app && chown appuser:appuser /app

# Set working directory to /app
WORKDIR /app

COPY ./ai_driver /app/ai_driver
RUN python3 -m pip install -e /app/ai_driver

# Change ownership of /app to appuser
RUN chown -R appuser:appuser /app

USER appuser

CMD ["/usr/bin/python3", "/app/ai_driver/ai_driver/main.py"]