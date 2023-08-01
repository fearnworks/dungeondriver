#! /usr/bin/env bash

# Create initial data in DB
python3 ./ai_driver/server/scripts/initial_data.py

# Let the DB start
python3 ./ai_driver/server/scripts/backend_pre_start.py

# Run migrations
alembic upgrade head
