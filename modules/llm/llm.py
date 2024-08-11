import httpcore
import tiktoken
from langchain_openai import ChatOpenAI

from config import settings
from modules.llm.helper import langfuse_handler
from modules.utils import logger


class LLM(object):
    def __init__(
        self,
        model: str = settings.OPENAI_MODEL_NAME,
        temperature: float = 0,
        max_tokens: int = 4096,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = self.get_api_key()
        self.base_url = self.get_base_url()
        self.llm = self.get_llm_model()

        # encoding
        self.encoding = tiktoken.get_encoding("o200k_base")

    def get_api_key(self):
        return settings.OPENAI_API_KEY

    def get_base_url(self):
        return settings.OPENAI_BASE_URL

    def get_llm_model(self):
        llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            api_key=self.api_key,
        )
        if self.base_url:
            llm.openai_api_base = self.base_url

        return llm

    async def get_chat_response(
        self,
        messages,
    ):
        if settings.DEBUG:
            output = await self.llm.ainvoke(
                messages,
                config={"callbacks": [langfuse_handler]},
            )
        else:
            output = await self.llm.ainvoke(messages)
        return output.content

    def num_tokens_from_message(
        self,
        message: str,
    ) -> int:
        return len(self.encoding.encode(message))

    def reduce_tokens_from_message(
        self,
        message: str,
        token_limits: int,
    ):
        message = self.encoding.encode(message)[:token_limits]
        return self.encoding.decode(message)


def get_llm(max_tokens: int) -> LLM:
    return LLM(max_tokens=max_tokens)
