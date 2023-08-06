"""
This module defines API endpoints related to chat such as fetching, creating, and updating chat sessions
"""
from loguru import logger
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ai_driver.cloud_llm.cloud_chat_agent import CloudChatAgent
from ai_driver.server import crud, schemas
from ai_driver.server.api import deps
from ai_driver.config import server_config
from ai_driver.server.redis import redis_client

router = APIRouter()


@router.post("/cloudllm", status_code=200, response_model=schemas.ChatBase)
def cloud_llm_endpoint(
    request: schemas.ChatRequest, db: Session = Depends(deps.get_db)
):
    # Fetch chat history from Redis
    logger.info(request)
    serialized_chat = redis_client.get(request.session_id)
    try:
        chat_history = (
            schemas.ChatHistory.parse_raw(serialized_chat.decode("utf-8"))
            if serialized_chat
            else schemas.ChatHistory(
                history=[schemas.ChatPair(human="Hi", ai="How are you?")],
                session_id=request.session_id,
            )
        )
    except Exception as err:
        logger.error(f"Error deserializing chat history: {err}")
        chat_history = schemas.ChatHistory(
            history=[schemas.ChatPair(human="Hi", ai="How are you?")],
            session_id=request.session_id,
        )

    logger.info(chat_history)
    agent = CloudChatAgent(history=[pair for pair in chat_history.history])
    response = agent.get_completion(request.query)
    result = response["result"]

    if isinstance(result, str):
        # Update the chat history
        new_chat_pair = schemas.ChatPair(human=request.query, ai=result)
        chat_history.history.append(new_chat_pair)
    else:
        # Handle unexpected response type if necessary
        logger.warning(f"Unexpected response type: {type(result)}")

    # Save entire chat history in Redis
    redis_client.set(name=request.session_id, value=chat_history.json())
    response_model = schemas.ChatBase(
        query=request.query, result=result, session_id=request.session_id
    )
    logger.info(response_model)
    return response_model


@router.post("/cloudllm/history", status_code=200, response_model=schemas.ChatHistory)
def get_chat_history(request: schemas.ChatHistoryRequest):
    # Fetch chat history from Redis using the session_id
    serialized_chat = redis_client.get(request.session_id)
    logger.info(serialized_chat)
    if not serialized_chat:
        # If no chat history is found for the session_id, return an empty history
        return schemas.ChatHistory(history=[], session_id=request.session_id)

    # Deserialize the chat history
    try:
        chat_history = schemas.ChatHistory.parse_raw(serialized_chat.decode("utf-8"))
    except Exception as e:
        logger.error(f"Error deserializing chat history: {e}")
        # If there's a deserialization error, return an empty history
        return schemas.ChatHistory(history=[], session_id=request.session_id)

    return chat_history
