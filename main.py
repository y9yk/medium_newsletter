import asyncio

import click

from modules.processor import Processor
from modules.utils import logger


@click.command()
@click.option("--topics", required=True, type=click.STRING)
@click.option("--publish_status", required=False, type=click.STRING, default="draft")
def execute(topics: str, publish_status: str):
    topics = [v.strip() for v in topics.split(",")]
    logger.debug(f"topics: {topics}")
    logger.debug(f"publish_status: {publish_status}")

    # create event loop
    loop = asyncio.get_event_loop()

    processor = Processor(topics=topics, publish_status=publish_status)
    loop.run_until_complete(processor.run())

    # close event loop
    loop.close()


if __name__ == "__main__":
    execute()
