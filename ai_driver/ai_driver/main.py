import os 
from typing import List, Iterable, Dict
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from loguru import logger 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

LANGCHAIN_TRACING_V2 = os.environ.get("LANGCHAIN_TRACING_V2")
LANGCHAIN_PROJECT = os.environ.get("LANGCHAIN_PROJECT")
LANGCHAIN_ENDPOINT = os.environ.get("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY")

import time

from langsmith import Client

def get_default_langsmith_client():
    return Client(api_url=LANGCHAIN_ENDPOINT, api_key=LANGCHAIN_API_KEY)

def load(dir_path:str, glob_pattern:str) -> Iterable[Document]:    
    loader = DirectoryLoader(dir_path, glob=glob_pattern, loader_cls=PyPDFLoader) # Note: If you're using PyPDFLoader then it will split by page for you already
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
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        logger.info(type(documents))
        logger.info(f"Splitting {len(documents)} documents into chunks of size {chunk_size} with overlap {chunk_overlap}")
        logger.info(documents)
        texts = text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(texts)}")
        return texts


def get_default_local_download() -> List[Document]:
    dir_path = "/app/ai_driver/data"
    glob_pattern = "./*.pdf"

    chunks = load(dir_path, glob_pattern)
    texts = split(chunks, chunk_size=1000, chunk_overlap=200)
    return texts

####

import textwrap
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from loguru import logger 



def wrap_text_preserve_newlines(text, width=110):
    lines = text.split('\n')
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
    wrapped_text = '\n'.join(wrapped_lines)
    return wrapped_text

def process_llm_response(llm_response):
    logger.info(wrap_text_preserve_newlines(llm_response['result']))
    logger.info('\nSources:')
    for source in llm_response["source_documents"]:
        logger.info(source.metadata['source'])

def query_documents(qa_chain, query):
    llm_response = qa_chain(query)
    process_llm_response(llm_response)

#### FAISS
def embed_FAISS_from_documents(documents: Iterable[Document], embedding_model_name: str, embedding_model_kwargs: Dict)-> FAISS:
    logger.info("Creating embeddings")
    start_time = time.time()
    instructor_embeddings = HuggingFaceInstructEmbeddings(model_name=embedding_model_name, model_kwargs=embedding_model_kwargs, cache_folder="")
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


def local_download_pipeline():
    texts = get_default_local_download()

    embedding_model_name = "hkunlp/instructor-xl"
    embedding_model_kwargs = {"device": "cuda"}

    vector_store = embed_FAISS_from_documents(texts, embedding_model_name, embedding_model_kwargs)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    client = get_default_langsmith_client()
    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(client=client, temperature=0.2), 
                                    chain_type="stuff", 
                                    retriever=retriever, 
                                    verbose=True,
                                    return_source_documents=True)

    query_documents(qa_chain, "How do saving throws work?")
####
if __name__ == "__main__":
    local_download_pipeline()