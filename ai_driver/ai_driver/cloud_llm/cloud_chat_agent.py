from typing import Type
from dataclasses import dataclass
from loguru import logger
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from typing import List
from ai_driver.langsmith_config import get_client
from ai_driver.server.schemas.chat import ChatPair, ChatHistory


@dataclass
class CloudChatConfig:
    llm: Type[ChatOpenAI] = ChatOpenAI
    temperature: float = 0.0
    model: str = "gpt-3.5-turbo-0613"
    verbose: bool = False


class CloudChatAgent:
    def __init__(
        self, history: List[ChatPair], config: CloudChatConfig = CloudChatConfig()
    ):
        self.llm: ChatOpenAI = ChatOpenAI(
            client=get_client(),
            temperature=config.temperature,
            model=config.model,
        )
        self.history = history
        self.memory = ConversationBufferMemory(return_messages=True)
        for turn in self.history:
            self.memory.save_context({"input": turn.human}, {"output": turn.ai})
        logger.info(self.memory.load_memory_variables({}))

        self.chat = ConversationChain(
            llm=self.llm, memory=self.memory, verbose=config.verbose
        )
        self.temperature = config.temperature
        self.model = config.model
        self.config = config

    def get_completion(self, prompt):
        logger.info(f"Prompt: {prompt}")
        response = self.chat.predict(input=prompt)
        logger.info(f"Response: {response}")
        return {"query": prompt, "result": response}
