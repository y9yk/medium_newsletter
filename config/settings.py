import os
from functools import lru_cache
from os import path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    기본 Configuration
    """

    PROJECT_ROOT: str = path.dirname(
        path.dirname(
            (path.abspath(__file__)),
        ),
    )

    PROJECT_NAME: str = "medium_newsletter"
    PROJECT_DESC: str = ""

    DEBUG: bool = True

    # token
    MEDIUM_ACCESS_TOKEN: str = ""
    GOOGLE_SERVICE_ACCOUNT_FILEPATH: str = f"{PROJECT_ROOT}/credential"
    GOOGLE_SERVICE_ACCOUNT_FILENAME: str = "gcloud.json"

    TIMEOUT: int = 10
    TECHNEWS_GENERATOR_TIMEOUT: int = 600
    USER_AGENT: str = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    )

    SEED_FILENAME: str = "awesome_research_sites"
    READING_LIST_FILENAME: str = "reading_list"
    TITLE_LIST_FILENAME: str = "title_list"

    OPENAI_MODEL_NAME: str = "gpt-4o-mini"
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    OPENAI_TOKEN_LIMIT: int = 128000
    MAX_TOKENS: int = 4096 * 2
    EPSILON: int = 100

    # langfuse integration
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = ""

    MEDIUM_API_BASE_URL: str = "https://api.medium.com"
    MEDIUM_API_GET_USER_URL: str = "/v1/me"

    INTRODUCTION_CONTENT_TYPE: str = "introduction"
    MAIN_BODY_CONTENT_TYPE: str = "main_body"
    TITLE_CONTENT_TYPE: str = "title"
    TAG: str = "y9yk-technews"

    SAMPLE_K: int = 10

    class Config:
        env_prefix = ""
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/.env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings: Settings = get_settings()
