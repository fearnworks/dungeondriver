from loguru import logger
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

from ai_driver.langsmith_config import get_client
from ai_driver.vector_storage.faiss_manager import embed_FAISS_from_documents
from ai_driver.local_loader import get_default_local_download
from ai_driver.retrieval.qa import qa_pipeline
from ai_driver.instruct import get_instruct_config, InstructConfig

from ai_driver.config import server_config


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
    model: OpenAI = OpenAI(
        client=get_client(),
        temperature=0.0,
        model="gpt-3.5-turbo-0613",
    )
    response = qa_pipeline("How do saving throws work?", retriever, model)
    return response
