FROM python:3.11

RUN python3 -m pip install --upgrade pip

# Create appuser
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# Create app directory and change ownership to appuser
RUN mkdir /app && chown appuser:appuser /app

# Set working directory to /app
WORKDIR /app

COPY ./dungeon_driver /app/dungeon_driver
RUN python3 -m pip install -e /app/dungeon_driver

# Change ownership of /app to appuser
RUN chown -R appuser:appuser /app

USER appuser

CMD ["/usr/bin/python3", "/app/dungeon_driver/dungeon_driver/main.py"]