from dotenv import load_dotenv, find_dotenv

from ai_driver.pipelines import (
    pinecone_pipeline,
    local_llm_pipeline,
    local_download_pipeline,
)

load_dotenv(find_dotenv())

####
if __name__ == "__main__":
    pinecone_pipeline()
    local_llm_pipeline()
    local_download_pipeline()
