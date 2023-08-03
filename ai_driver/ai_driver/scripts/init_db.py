from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from loguru import logger
from ai_driver.config import server_config


def run_db_build():
    # Build vector database
    loader = DirectoryLoader(
        server_config.DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader
    )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=server_config.CHUNK_SIZE, chunk_overlap=server_configCHUNK_OVERLAP
    )
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name=server_config.CHAT_EMBED_MODEL,
        model_kwargs={"device": "cpu"},
    )

    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(server_config.DB_PATH)


if __name__ == "__main__":
    run_db_build()
