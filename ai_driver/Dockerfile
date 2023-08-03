FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04
ENV PYTHONFAULTHANDLER=1
# Install dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y git vim build-essential python3-dev python3-pip procps net-tools tini && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip

# Create appuser
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# Create app directory and change ownership to appuser
RUN mkdir /app && \
    mkdir -p /home/appuser/.cache && \
    chown -R appuser:appuser /app /home/appuser
COPY ./requirements.txt /app/requirements.txt
COPY ./requirements-server.txt /app/requirements-server.txt
RUN --mount=type=cache,target=~/.cache/pip \
    pip install -r /app/requirements.txt && \
    pip install -r /app/requirements-server.txt
# # Set working directory to /app
WORKDIR /app



COPY . /app/ai_driver
RUN python3 -m pip install -e /app/ai_driver[server]

# Change ownership of /app to appuser
RUN chown -R appuser:appuser /app /home/appuser

USER appuser
WORKDIR /app/ai_driver
RUN chmod +x ./ai_driver/server/scripts/run.sh
ENTRYPOINT ["tini", "--", "./ai_driver/server/scripts/run.sh"]
# CMD ["tail", "-f", "/dev/null"]
