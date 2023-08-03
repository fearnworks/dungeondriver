from dataclasses import dataclass
from ai_driver.config import server_config


@dataclass
class InstructConfig:
    embed_model: str


def get_instruct_config():
    """Default Instruct Embedding Config"""
    config = InstructConfig(embed_model=server_config.INSTRUCT_EMBED_MODEL)
    return config
