# Compile requirements/requirements for dungeon_driver
cd ./dungeon_driver
pip-compile requirements/requirements.in --upgrade
pip-compile requirements/requirements-dev.in --upgrade
pip-compile requirements/requirements-test.in --upgrade
cd ..

# Compile requirements/requirements for ai_driver
cd ./ai_driver
pip-compile requirements/requirements.in --upgrade
pip-compile requirements/requirements-server.in --upgrade
pip-compile requirements/requirements-dev.in --upgrade
pip-compile requirements/requirements-test.in --upgrade
echo "Pin update complete."
cd ..
