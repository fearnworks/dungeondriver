FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Install dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y git vim build-essential python3-dev python3-pip && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip

# Create appuser
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# Create app directory and change ownership to appuser
RUN mkdir /app && \
    mkdir -p /home/appuser/.cache && \
    chown -R appuser:appuser /app /home/appuser
COPY ./pyproject.toml /app/pyproject.toml
# # Set working directory to /app
WORKDIR /app
RUN pip install .[server]


COPY . /app/ai_driver
RUN python3 -m pip install -e /app/ai_driver[server]

# Change ownership of /app to appuser
RUN chown -R appuser:appuser /app /home/appuser

USER appuser
WORKDIR /app/ai_driver
RUN chmod +x ./ai_driver/server/scripts/run.sh
CMD ["./ai_driver/server/scripts/run.sh"]
# CMD ["tail", "-f", "/dev/null"]
