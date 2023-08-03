from typing import List, Iterable
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from loguru import logger
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI

from ai_driver.langsmith_config import get_client
from ai_driver.vector_storage.faiss_manager import embed_FAISS_from_documents
from ai_driver.retrieval.qa import qa_pipeline
from ai_driver.instruct import get_instruct_config, InstructConfig

from ai_driver.config import server_config


def load(dir_path: str, glob_pattern: str) -> Iterable[Document]:
    loader = DirectoryLoader(
        dir_path, glob=glob_pattern, loader_cls=PyPDFLoader
    )  # Note: If you're using PyPDFLoader then it will split by page for you already
    documents = loader.load()
    logger.info(f"Loaded {len(documents)} documents from {dir_path}")
    return documents


def split(documents: Iterable[Document], chunk_size, chunk_overlap) -> List[Document]:
    """
    Splits the specified list of PyPDFLoader instances into text chunks using a recursive character text splitter.

    Args:
        documents  (Iterable[Document]): The documents to split.
        chunk_size (int): The size of each text chunk.
        chunk_overlap (int): The overlap between adjacent text chunks.

    Returns:
        List[str]: A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    logger.info(type(documents))
    logger.info(
        f"Splitting {len(documents)} documents into chunks of size {chunk_size} with overlap {chunk_overlap}"
    )
    logger.info(documents)
    texts = text_splitter.split_documents(documents)
    logger.info(f"Split {len(documents)} documents into {len(texts)}")
    return texts


def local_download_pipeline(config=None):
    """Example local store pipeline"""

    logger.info("Local download pipeline: FAISS")
    dir_path = server_config.DATA_PATH
    texts = get_default_local_download(dir_path=dir_path)
    config: InstructConfig = get_instruct_config()

    embedding_model_name = config.embed_model
    embedding_model_kwargs = {"device": "cuda"}

    vector_store = embed_FAISS_from_documents(
        texts, embedding_model_name, embedding_model_kwargs
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    model: ChatOpenAI = ChatOpenAI(
        client=get_client(),
        temperature=0.0,
        model="gpt-3.5-turbo-0613",
    )
    response = qa_pipeline("How do saving throws work?", retriever, model)
    return response


def get_default_local_download(dir_path: str) -> List[Document]:
    """Default document list for local download"""
    glob_pattern = "./*.pdf"

    chunks = load(dir_path, glob_pattern)
    texts = split(chunks, chunk_size=1000, chunk_overlap=200)
    return texts
