from dataclasses import dataclass
import box
import yaml


@dataclass
class InstructConfig:
    embed_model: str


def get_instruct_config():
    """Default Instruct Embedding Config"""
    with open("config/config.yml", "r", encoding="utf8") as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))
        config = InstructConfig(embed_model=cfg.INSTRUCT_EMBED_MODEL)
        return config
