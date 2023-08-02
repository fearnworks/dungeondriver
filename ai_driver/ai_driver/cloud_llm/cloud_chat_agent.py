from typing import Type
from dataclasses import dataclass
from loguru import logger
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from ai_driver.langsmith_config import get_default_langsmith_client


@dataclass
class CloudChatConfig:
    llm: Type[ChatOpenAI] = ChatOpenAI
    temperature: float = 0.0
    model: str = "gpt-3.5-turbo-0613"
    verbose: bool = False
    langsmith: bool = True


class CloudChatAgent:
    def __init__(self, config: CloudChatConfig = CloudChatConfig()):
        if config.langsmith:
            self.llm: ChatOpenAI = ChatOpenAI(
                client=get_default_langsmith_client(),
                temperature=config.temperature,
                model=config.model,
            )
        else:
            self.llm: ChatOpenAI = config.llm(
                temperature=config.temperature, model=config.model
            )
        self.chat = self.llm  # backwards compat
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm, memory=self.memory, verbose=config.verbose
        )
        self.temperature = config.temperature
        self.model = config.model
        self.config = config

    def get_completion(self, prompt):
        logger.info(f"Prompt: {prompt}")
        messages = [{"role": "user", "content": prompt}]
        response = self.chat.predict(prompt)
        logger.info(f"Response: {response}")
        return {"query": prompt, "result": response}
