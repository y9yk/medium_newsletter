import random
from uuid import uuid4

from config import settings
from modules.feeds import (
    get_seed_data_manager,
    get_feed_data_parser,
    get_feed_data_loader,
)
from modules.llm import get_technews_generator
from modules.medium import get_medium_poster
from modules.utils import logger, log_step
from modules.post_processor import get_postproc


class Processor(object):
    def __init__(self, topics, publish_status: str = "draft"):
        self.topics = topics
        self.publish_status = publish_status

        # workers
        self.seed_data_manager = get_seed_data_manager()
        self.feed_data_parser = get_feed_data_parser()
        self.feed_data_loader = get_feed_data_loader()
        self.technews_generator = get_technews_generator()
        self.medium_poster = get_medium_poster()
        self.postproc = get_postproc()

    async def run(self):
        log_step("get_seed_data")
        seed_urls = self.seed_data_manager.get_seed_urls()
        logger.debug(seed_urls)

        log_step("parse_feed_data")
        feeds = []
        for name, url in seed_urls:
            logger.debug(f"parsing: {name}")
            feeds.extend(self.feed_data_parser.parse_feed_data(url=url))

        log_step("filter feeds not in reading_list -> sampling (TODO to extract favorate contents for me)")
        reading_list = self.seed_data_manager.get_reading_list()
        feeds = list(
            filter(
                lambda x: x.get("link") not in reading_list,
                feeds,
            )
        )
        log_step("filter feeds by summary length")
        feeds = list(
            filter(
                lambda x: x.get("summary") and len(x.get("summary")) > 0,
                feeds,
            )
        )

        log_step("inspect filter length")
        if len(feeds) == 0:
            logger.warning("There is no feed in filtered feeds")
            return

        # --------------------------------------------------------------

        feeds = random.sample(feeds, k=settings.SAMPLE_K)

        log_step("technews_generator")
        ret = await self.technews_generator.process(
            context=feeds,
            topics=self.topics,
            title_list=self.seed_data_manager.get_title_list(),
        )

        #
        for item in ret:
            if item.get("type") == settings.TITLE_CONTENT_TYPE:
                title = item.get("content")
            if item.get("type") == settings.MAIN_BODY_CONTENT_TYPE:
                content = item.get("content")

            # debugging
            if settings.DEBUG:
                with open(f"{settings.PROJECT_ROOT}/resources/{item.get('type')}-{str(uuid4())}.txt", "w") as f:
                    f.write(item.get("content"))

        if title and content:
            log_step("append title to content")
            content = f"""# {title}\n\n\n\n\n\n{content}"""

            log_step("medium posting")
            user_id = await self.medium_poster.get_user_id()
            response = await self.medium_poster.post(
                user_id=user_id,
                title=title,
                content=content,
                tags=[settings.TAG],
                publish_status=self.publish_status,
            )

            logger.debug(response)

            log_step("post-processing")
            self.postproc.record_reading_list(feeds)
            self.postproc.record_title_list(title)
