"""
This module defines API endpoints related to characters such as fetching, creating, updating,
searching characters and fetching character ideas from Reddit.
"""

import asyncio
from typing import Any, Optional
from loguru import logger
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ai_driver.cloud_llm.cloud_chat_agent import CloudChatAgent
from ai_driver.image_generation.prompt_generation.sd_prompt_agent import (
    get_default_sd_agent,
)
from ai_driver.server import schemas
from ai_driver.server.api import deps

router = APIRouter()


@router.post("/prompt", status_code=200, response_model=schemas.SDPromptGeneration)
def sd_prompt_endpoint(
    request: schemas.ChatRequest, db: Session = Depends(deps.get_db)
):
    sd_agent = get_default_sd_agent()
    query = request.query
    prompt = sd_agent.get_completion(query)
    eval_resp = sd_agent.rate(prompt["result"])
    logger.info(eval_resp)
    evaluations = schemas.SDEvaluations.parse_obj(eval_resp)
    prompt_gen = schemas.SDPromptGeneration(
        prompt=prompt["result"], evaluations=evaluations
    )
    return prompt_gen
