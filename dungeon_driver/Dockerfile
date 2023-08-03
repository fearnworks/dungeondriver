FROM python:3.11

RUN python3 -m pip install --upgrade pip

# Create appuser
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser

# Create app directory and change ownership to appuser
RUN mkdir /app && chown appuser:appuser /app
# Create home directory for appuser and change ownership
RUN mkdir /home/appuser && chown appuser:appuser /home/appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MPLCONFIGDIR /tmp/matplotlib

COPY ./pyproject.toml /app/pyproject.toml
# Set working directory to /app
RUN --mount=type=cache,target=~/.cache/pip \
    pip install /app

COPY . /app/dungeon_driver
WORKDIR /app/dungeon_driver
RUN python3 -m pip install -e .


USER appuser
CMD ["python3", "dungeon_driver/main.py"]
# CMD ["tail", "-f", "/dev/null"]
