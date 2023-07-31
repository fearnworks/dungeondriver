import os
import timeit
from loguru import logger
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA


from ai_driver.vector_storage.pinecone_manager import (
    get_default_pinecone_session,
    PineconeConfig,
)
from ai_driver.langsmith_config import get_default_langsmith_client
from ai_driver.vector_storage.faiss_manager import embed_FAISS_from_documents
from ai_driver.local_loader import get_default_local_download
from ai_driver.qa import query_documents
from ai_driver.instruct import get_instruct_config, InstructConfig
from ai_driver.local_llm.ggml_pipeline import setup_local_qa_db, get_default_qa_config


def pinecone_pipeline():
    """Example Pinecone Pipeline"""
    logger.info("Pinecone Pipeline")
    config = PineconeConfig(
        openai_key=os.getenv("OPENAI_API_KEY"),
        pinecone_key=os.getenv("PINECONE_API_KEY"),
        pinecone_env=os.getenv("PINECONE_API_ENV"),
        index_name=os.getenv("PINECONE_INDEX_NAME"),
    )
    logger.info(config)
    vector_store = get_default_pinecone_session(config).docsearch
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    client = get_default_langsmith_client()
    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(client=client, temperature=0.2),
        chain_type="stuff",
        retriever=retriever,
        verbose=True,
        return_source_documents=True,
    )
    query_documents(qa_chain, "How do saving throws work?")


def local_llm_pipeline():
    """Example Local LLM Pipeline"""

    query = "How do saving throws work?"

    # Setup DBQA
    start = timeit.default_timer()
    config = get_default_qa_config()
    dbqa = setup_local_qa_db(config)
    response = dbqa({"query": query})
    end = timeit.default_timer()

    logger.info(f'\nAnswer: {response["result"]}')
    logger.info("=" * 50)

    # Process source documents
    source_docs = response["source_documents"]
    for i, doc in enumerate(source_docs):
        logger.info(f"\nSource Document {i+1}\n")
        logger.info(f"Source Text: {doc.page_content}")
        logger.info(f'Document Name: {doc.metadata["source"]}')
        logger.info(f'Page Number: {doc.metadata["page"]}\n')
        logger.info("=" * 60)

    logger.info(f"Time to retrieve response: {end - start}")


def local_download_pipeline(config=None):
    """Example local store pipeline"""
    logger.info("Local download pipeline: FAISS")
    texts = get_default_local_download()
    config: InstructConfig = get_instruct_config()

    embedding_model_name = config.embed_model
    embedding_model_kwargs = {"device": "cuda"}

    vector_store = embed_FAISS_from_documents(
        texts, embedding_model_name, embedding_model_kwargs
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    client = get_default_langsmith_client()
    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(client=client, temperature=0.2),
        chain_type="stuff",
        retriever=retriever,
        verbose=True,
        return_source_documents=True,
    )

    query_documents(qa_chain, "How do saving throws work?")
