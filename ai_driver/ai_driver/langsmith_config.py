import os

LANGCHAIN_TRACING_V2 = os.environ.get("LANGCHAIN_TRACING_V2")
LANGCHAIN_PROJECT = os.environ.get("LANGCHAIN_PROJECT")
LANGCHAIN_ENDPOINT = os.environ.get("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY")

from langsmith import Client


def get_default_langsmith_client():
    """Default client for langchain logging"""
    return Client(api_url=LANGCHAIN_ENDPOINT, api_key=LANGCHAIN_API_KEY)
