"""
This module defines API endpoints related to characters such as fetching, creating, updating,
searching characters and fetching character ideas from Reddit.
"""
from loguru import logger
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ai_driver.cloud_llm.cloud_chat_agent import CloudChatAgent
from ai_driver.local_llm.ggml_pipeline import local_llm_qa_pipeline
from ai_driver.server import crud, schemas
from ai_driver.server.api import deps
from ai_driver.local_loader import local_download_pipeline
from ai_driver.cloud_llm.cloud_qa import pinecone_qa_pipeline
from ai_driver.config import server_config

router = APIRouter()


@router.get("/local_download_pipline")
def local_endpoint(
    db: Session = Depends(deps.get_db),
):
    local_download_pipeline(dir_path=server_config.DATA_PATH)


@router.post("/pinecone", status_code=200, response_model=schemas.ChatBase)
def pinecone_endpoint(request: schemas.ChatRequest, db: Session = Depends(deps.get_db)):
    response = pinecone_qa_pipeline(request.query)
    result = schemas.ChatBase(query=request.query, result=response)
    logger.info(result)
    return result


@router.post("/local_llm", status_code=200, response_model=schemas.ChatBase)
def local_llm_endpoint(
    request: schemas.ChatRequest, db: Session = Depends(deps.get_db)
):
    response = local_llm_qa_pipeline(request.query)
    result = schemas.ChatBase(query=request.query, result=response)
    logger.info(result)
    return result


@router.post("/cloudllm", status_code=200, response_model=schemas.ChatBase)
def cloud_llm_endpoint(
    request: schemas.ChatRequest, db: Session = Depends(deps.get_db)
):
    agent = CloudChatAgent()
    response = agent.get_completion(request.query)
    # result = schemas.ChatBase(query=query, result=response)
    # logger.info(result)
    return response
