import os
from loguru import logger
from langsmith import Client as LangsmithClient

LANGCHAIN_TRACING_V2 = os.environ.get("LANGCHAIN_TRACING_V2")
LANGCHAIN_PROJECT = os.environ.get("LANGCHAIN_PROJECT")
LANGCHAIN_ENDPOINT = os.environ.get("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY")

from ai_driver.config import server_config


def get_client():
    """Default client for langchain"""
    logger.info(server_config.LANGSMITH_LOGGING)
    if server_config.LANGSMITH_LOGGING:
        return LangsmithClient(api_url=LANGCHAIN_ENDPOINT, api_key=LANGCHAIN_API_KEY)
    else:
        logger.info("Langsmith disabled")
        return None
