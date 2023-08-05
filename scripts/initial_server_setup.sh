docker network create dd-network

python3 -m venv .server_venv && source .server_venv/bin/activate
python3 -m pip install -r ./ai_driver/requirements.txt

python3 ./ai_driver/ai_driver/scripts/download_model.py
python3 ./ai_driver/ai_driver/scripts/init_vectorstore.py
