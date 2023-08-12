#!/bin/bash

# Compile requirements/requirements for dungeon_driver
cd ./dungeon_driver
pip-compile requirements/requirements.in
pip-compile requirements/requirements-dev.in
pip-compile requirements/requirements-test.in
cd ..

# Compile requirements/requirements for ai_driver
cd ./ai_driver
pip-compile requirements/requirements.in
pip-compile requirements/requirements-server.in
pip-compile requirements/requirements-dev.in
pip-compile requirements/requirements-test.in
echo "Pin update complete."
cd ..
