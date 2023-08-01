"""
This module defines API endpoints related to characters such as fetching, creating, updating,
searching characters and fetching character ideas from Reddit.
"""

import asyncio
from typing import Any, Optional
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
import httpx

from ai_driver.server import crud, schemas
from ai_driver.server.api import deps
from ai_driver.pipelines import (
    pinecone_pipeline,
    local_llm_pipeline,
    local_download_pipeline,
)

# from app.clients.reddit import RedditClient
# from app.models.user import User
# from app.schemas.character import (Character, CharacterCreate,
#                                    CharacterSearchResults,
#                                    CharacterUpdateRestricted)

router = APIRouter()


chat_router = APIRouter()


@router.get("/local_download_pipline")
def local_endpoint(
    db: Session = Depends(deps.get_db),
):
    local_download_pipeline()


@router.get("/pinecone/{query}", status_code=200, response_model=schemas.ChatBase)
def pinecone_endpoint(query: str, db: Session = Depends(deps.get_db)):
    response = pinecone_pipeline(query)
    logger.info(response)
    return response


@router.get("/local_llm/{query}", status_code=200, response_model=schemas.ChatBase)
def local_llm_endpoint(query: str, db: Session = Depends(deps.get_db)):
    response = local_llm_pipeline(query)
    logger.info(response)
    return response
