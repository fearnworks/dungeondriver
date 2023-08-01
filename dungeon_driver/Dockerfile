FROM python:3.11

RUN python3 -m pip install --upgrade pip

# Create appuser
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# Create app directory and change ownership to appuser
RUN mkdir /app && chown appuser:appuser /app

COPY ./pyproject.toml /app/pyproject.toml
# Set working directory to /app
RUN pip install /app

COPY . /app/dungeon_driver
WORKDIR /app
RUN python3 -m pip install -e .

# Change ownership of /app to appuser
RUN chown -R appuser:appuser /app

USER appuser
WORKDIR /app/dungeon_driver
CMD ["python3", "dungeon_driver/main.py"]
# CMD ["tail", "-f", "/dev/null"]
