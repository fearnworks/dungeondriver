from langchain.llms import CTransformers
import box
import yaml
from dataclasses import dataclass


@dataclass
class GGMLConfig:
    model_path: str
    model_type: str
    max_new_tokens: int
    temperature: float = 0.7


def build_ggml_llm(config: GGMLConfig) -> CTransformers:
    llm = CTransformers(
        model=config.model_path,
        model_type=config.model_type,
        config={
            "max_new_tokens": config.max_new_tokens,
            "temperature": config.temperature,
        },
    )
    return llm


def get_default_ggml_config():
    # Import config vars
    with open("config/config.yml", "r", encoding="utf8") as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))
        config = GGMLConfig(
            model_path=cfg.LLM_MODEL_BIN_PATH,
            model_type=cfg.MODEL_TYPE,
            max_new_tokens=cfg.MAX_NEW_TOKENS,
            temperature=cfg.TEMPERATURE,
        )
        return config
