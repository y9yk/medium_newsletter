from datetime import datetime
from pytz import timezone

from modules.feeds import get_seed_data_manager
from modules.utils import logger


class PostProcessor(object):

    def __init__(self):
        self.seed_data_manager = get_seed_data_manager()

    def record_reading_list(self, feeds):
        feeds = [
            [
                item.get("link"),
                datetime.now(timezone("Asia/Seoul")).strftime("%Y%m%d"),
            ]
            for item in feeds
        ]
        logger.debug(f"updated links: {feeds}")

        self.seed_data_manager.record_reading_list(feeds=feeds)

    def record_title_list(self, title):
        logger.debug(f"updated title: {title}")

        self.seed_data_manager.record_title_list(
            title=[
                [
                    title,
                    datetime.now(timezone("Asia/Seoul")).strftime("%Y%m%d"),
                ]
            ]
        )


postproc = PostProcessor()


def get_postproc() -> PostProcessor:
    return postproc
