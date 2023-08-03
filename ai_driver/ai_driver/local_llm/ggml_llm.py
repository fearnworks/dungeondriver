from langchain.llms import CTransformers
from ai_driver.config import server_config
from dataclasses import dataclass


@dataclass
class GGMLConfig:
    model_path: str
    model_type: str
    max_new_tokens: int
    temperature: float = 0.7
    gpu_layers: int = 0


def build_ggml_llm(config: GGMLConfig) -> CTransformers:
    llm = CTransformers(
        model=config.model_path,
        model_type=config.model_type,
        config={
            "max_new_tokens": config.max_new_tokens,
            "temperature": config.temperature,
            "gpu_layers": config.gpu_layers,
        },
    )
    return llm


def get_default_ggml_config():
    # Import config vars
    config = GGMLConfig(
        model_path=server_config.LLM_MODEL_BIN_PATH,
        model_type=server_config.MODEL_TYPE,
        max_new_tokens=server_config.MAX_NEW_TOKENS,
        temperature=server_config.TEMPERATURE,
        gpu_layers=server_config.GGML_GPU_LAYERS,
    )
    return config
