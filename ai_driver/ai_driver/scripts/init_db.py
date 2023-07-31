import yaml
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from loguru import logger
import box

# Import config vars
with open("config/config.yml", "r", encoding="utf8") as ymlfile:
    logger.info("Loading config")
    cfg = box.Box(yaml.safe_load(ymlfile))
    logger.info(cfg)


def run_db_build():
    # Build vector database
    loader = DirectoryLoader(cfg.DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg.CHUNK_SIZE, chunk_overlap=cfg.CHUNK_OVERLAP
    )
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name=cfg.CHAT_EMBED_MODEL,
        model_kwargs={"device": "cpu"},
    )

    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(cfg.DB_PATH)


if __name__ == "__main__":
    run_db_build()
