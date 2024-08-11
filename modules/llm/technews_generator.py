import json
import asyncio
import traceback

from typing import List

from config import settings
from modules.llm import (
    get_llm,
    generate_newsletter_title,
    generate_newsletter_main_body,
    LLM,
)
from modules.utils import logger


class TechNewsGenerator(object):
    def __init__(self):
        self.client: LLM = get_llm(max_tokens=settings.MAX_TOKENS)
        self.role = (
            "당신은 주어진 피드 정보를 요약하여 글을 작성하고, 이를 블로그에 업데이트하는 Tech 블로그 운영자입니다."
        )

    async def generate_newsletter_title(self, context, title_list):
        ret = ""
        try:
            # content
            context = json.dumps(
                [
                    {
                        "title": item.get("title"),
                    }
                    for item in list(
                        filter(
                            lambda x: x.get("link") is not None,
                            context,
                        )
                    )
                ],
                ensure_ascii=False,
            )

            # process
            while True:
                ret = await self.client.get_chat_response(
                    messages=[
                        {
                            "role": "system",
                            "content": self.role,
                        },
                        {
                            "role": "user",
                            "content": generate_newsletter_title(context),
                        },
                    ],
                )

                # condition
                if ret not in title_list:
                    break
        except Exception as e:
            logger.error(f"Error in generate_report: {e}")
        return {
            "type": settings.TITLE_CONTENT_TYPE,
            "content": ret,
        }

    async def generate_newsletter_main_body(self, context: str, topics: List):
        ret = ""
        try:
            # get content
            context = json.dumps(
                [
                    {
                        "title": item.get("title"),
                        "link": item.get("link"),
                        "summary": item.get("summary"),
                        "tags": item.get("tags"),
                        "published": item.get("published"),
                        "publisher": item.get("publisher"),
                    }
                    for item in list(
                        filter(
                            lambda x: x.get("link") is not None,
                            context,
                        )
                    )
                ],
                ensure_ascii=False,
            )
            message = (
                [
                    {
                        "role": "system",
                        "content": self.role,
                    },
                    {
                        "role": "user",
                        "content": generate_newsletter_main_body(context, topics),
                    },
                ],
            )
            message_token_size = self.client.num_tokens_from_message(message=json.dumps(message, ensure_ascii=False))
            if message_token_size > settings.OPENAI_TOKEN_LIMIT:
                # reduce context_token_size (consider topic token size)
                context_token_size = self.client.num_tokens_from_message(message=context)
                topic_token_size = self.client.num_tokens_from_message(message=",".join(topics))
                context_token_size = (
                    context_token_size
                    - (message_token_size - settings.OPENAI_TOKEN_LIMIT)
                    - topic_token_size
                    - settings.MAX_TOKENS
                    - settings.EPSILON
                )

                # reconstruct message
                context = self.client.reduce_tokens_from_message(message=context, token_limits=context_token_size)
                context = generate_newsletter_main_body(context, topics)
            else:
                context = generate_newsletter_main_body(context, topics)

            # process
            ret = await self.client.get_chat_response(
                messages=[
                    {
                        "role": "system",
                        "content": self.role,
                    },
                    {
                        "role": "user",
                        "content": context,
                    },
                ],
            )
        except Exception as e:
            logger.error(f"Error in generate_report: {e}")
        return {
            "type": settings.MAIN_BODY_CONTENT_TYPE,
            "content": ret,
        }

    async def process(self, context, topics: List, title_list: List = []):
        try:
            # define tasks (exclude introduction)
            tasks = [
                asyncio.ensure_future(self.generate_newsletter_title(context, title_list)),
                asyncio.ensure_future(self.generate_newsletter_main_body(context, topics)),
            ]

            # process
            ret = await asyncio.wait_for(
                asyncio.gather(
                    *tasks,
                    return_exceptions=True,
                ),
                timeout=settings.TECHNEWS_GENERATOR_TIMEOUT,
            )
            return ret
        except:
            traceback.print_exc()
            return []


technews_generator = TechNewsGenerator()


def get_technews_generator() -> TechNewsGenerator:
    return technews_generator
