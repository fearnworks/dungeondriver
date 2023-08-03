#!/bin/bash

# Compile requirements for dungeon_driver
cd ./dungeon_driver
pip-compile requirements.in
pip-compile requirements-dev.in
pip-compile requirements-test.in
cd ..

# Compile requirements for ai_driver
cd ./ai_driver
pip-compile requirements.in
pip-compile requirements-server.in
pip-compile requirements-dev.in
pip-compile requirements-test.in
echo "Pin update complete."
cd ..
