#!/bin/bash

DOWNLOAD_MODEL=true
INIT_VECTORSTORE=true

while getopts "adv" opt; do
  case ${opt} in
    a )
      DOWNLOAD_MODEL=true
      INIT_VECTORSTORE=true
      ;;
    d )
      DOWNLOAD_MODEL=false
      ;;
    v )
      INIT_VECTORSTORE=false
      ;;
    \? )
      echo "Invalid option: -$OPTARG" 1>&2
      exit 1
      ;;
    : )
      echo "Option -$OPTARG requires an argument." 1>&2
      exit 1
      ;;
  esac
done

docker network create dd-network

python3 -m venv .server_venv && source .server_venv/bin/activate
python3 -m pip install -r ./ai_driver/requirements.txt

if [ "$DOWNLOAD_MODEL" = true ]; then
  python3 ./ai_driver/ai_driver/scripts/download_model.py
fi

if [ "$INIT_VECTORSTORE" = true ]; then
  python3 ./scripts/init_local_vectorstore.py
fi
