from config import settings
from modules.clients import make_request


class FeedDataLoader(object):

    def __init__(self):
        self.method = "get"
        self.headers = {"User-Agent": settings.USER_AGENT}

    async def get_data(self, url):
        data, status_code = await make_request(
            url=url,
            method=self.method,
            headers=self.headers,
            is_json_resp=False,
        )

        return (data, status_code)


feed_data_loader = FeedDataLoader()


def get_feed_data_loader() -> FeedDataLoader:
    return feed_data_loader
