from langchain.prompts import ChatPromptTemplate
from ai_driver.image_generation.prompt_generation.prompts import (
    SD_PROMPT_RATING_TEMPLATE,
)
from ai_driver.cloud_llm.cloud_chat_agent import CloudChatAgent, CloudChatConfig
from ai_driver.image_generation.prompt_generation.prompt_rating import SDPromptRating
from dataclasses import dataclass
from typing import Any


@dataclass
class SDAgentConfig(CloudChatConfig):
    temperature: float = 0.0
    sd_prompt_rating_template: str = SD_PROMPT_RATING_TEMPLATE


@dataclass
class SDPromptEvaluation:
    temperature: float
    generated_prompt: str
    evaluation: Any


class CloudSDAgent(CloudChatAgent):
    def __init__(self, config: SDAgentConfig):
        super().__init__(config=config)
        self.rate_template = ChatPromptTemplate.from_template(
            config.sd_prompt_rating_template
        )

    def rate(self, generated_prompt):
        # rate_template = ChatPromptTemplate.from_template(generated_prompt)
        rate_request = self.rate_template.format_messages(prompt=generated_prompt)
        response = self.chat(rate_request)
        return SDPromptRating.parse(response.content)


def get_default_sd_agent() -> CloudSDAgent:
    default_config = SDAgentConfig()
    return CloudSDAgent(default_config)
