from typing import List, Iterable, Dict
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from loguru import logger
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv, find_dotenv
from pinecone_manager import get_default_pinecone_session
from langsmith_config import get_default_langsmith_client
from faiss_manager import embed_FAISS_from_documents
from local_loader import get_default_local_download
from qa import query_documents
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

load_dotenv(find_dotenv())


def local_download_pipeline():
    logger.info("Local download pipeline: FAISS")
    texts = get_default_local_download()

    embedding_model_name = "hkunlp/instructor-xl"
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


def pinecone_pipeline():
    logger.info("Pinecone Pipeline")
    vector_store = get_default_pinecone_session("dungeondriver").docsearch
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


####
if __name__ == "__main__":
    pinecone_pipeline()
    # local_download_pipeline()
