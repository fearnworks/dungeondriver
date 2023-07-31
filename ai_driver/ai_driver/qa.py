import textwrap
from dataclasses import dataclass

from loguru import logger


@dataclass
class QADBConfig:
    db_path: str
    embed_model: str
    return_source: str
    vector_count: str


def wrap_text_preserve_newlines(text, width=110):
    lines = text.split("\n")
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
    wrapped_text = "\n".join(wrapped_lines)
    return wrapped_text


def process_llm_response(llm_response):
    logger.info(wrap_text_preserve_newlines(llm_response["result"]))
    logger.info("\nSources:")
    for source in llm_response["source_documents"]:
        logger.info(source.metadata)


def query_documents(qa_chain, query):
    llm_response = qa_chain(query)
    process_llm_response(llm_response)
