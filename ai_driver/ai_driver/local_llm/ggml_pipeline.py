from ai_driver.config import server_config


from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from ai_driver.local_llm.prompts import qa_template
from ai_driver.local_llm.ggml_llm import build_ggml_llm, get_default_ggml_config
from ai_driver.qa import QADBConfig


def set_qa_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(
        template=qa_template, input_variables=["context", "question"]
    )
    return prompt


def build_retrieval_qa(llm, prompt, vectordb, config: QADBConfig):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(search_kwargs={"k": config.vector_count}),
        return_source_documents=config.return_source,
        chain_type_kwargs={"prompt": prompt},
    )
    return qa_chain


def setup_local_qa_db(config: QADBConfig, device: str = "cuda"):
    # Set device to cpu for cpu inference

    embeddings = HuggingFaceEmbeddings(
        model_name=config.embed_model, model_kwargs={"device": device}
    )
    vectordb = FAISS.load_local(config.db_path, embeddings)

    ggml_config = get_default_ggml_config()
    llm = build_ggml_llm(ggml_config)
    qa_prompt = set_qa_prompt()
    dbqa = build_retrieval_qa(llm, qa_prompt, vectordb, config)

    return dbqa


def get_default_qa_config():
    config = QADBConfig(
        db_path=server_config.DB_PATH,
        embed_model=server_config.CHAT_EMBED_MODEL,
        return_source=server_config.RETURN_SOURCE_DOCUMENTS,
        vector_count=server_config.VECTOR_COUNT,
    )
    return config
