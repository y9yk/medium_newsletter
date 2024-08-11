import asyncio

import click

from modules.processor import Processor
from modules.utils import logger


@click.command()
@click.option("--topics", required=True, type=click.STRING)
def execute(topics: str):
    topics = [v.strip() for v in topics.split(",")]
    logger.debug(f"topics: {topics}")

    # create event loop
    loop = asyncio.get_event_loop()

    processor = Processor(topics=topics)
    loop.run_until_complete(processor.run())

    # close event loop
    loop.close()


if __name__ == "__main__":
    execute()
