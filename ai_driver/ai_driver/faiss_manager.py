from loguru import logger
from typing import Dict, Iterable
from langchain.vectorstores import FAISS
import time
from langchain.schema import Document
from langchain.embeddings import HuggingFaceInstructEmbeddings


def embed_FAISS_from_documents(
    documents: Iterable[Document],
    embedding_model_name: str,
    embedding_model_kwargs: Dict,
) -> FAISS:
    logger.info("Creating embeddings")
    start_time = time.time()
    instructor_embeddings = HuggingFaceInstructEmbeddings(
        model_name=embedding_model_name,
        model_kwargs=embedding_model_kwargs,
        cache_folder="",
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Embeddings created in {elapsed_time:.2f} seconds")

    logger.info("Creating vector store")
    start_time = time.time()
    db_instructEmbedd = FAISS.from_documents(documents, instructor_embeddings)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Vector store created in {elapsed_time:.2f} seconds")

    logger.info("Vector store created")
    return db_instructEmbedd
