import feedparser

from typing import List


class FeedDataParser(object):

    def parse_feed_data(self, url) -> List:
        try:
            data = feedparser.parse(url_file_stream_or_string=url)

            assert data
            assert data.get("entries") and len(data.get("entries")) > 0

            # get items
            items = data.get("entries")
            return items
        except:
            return []


feed_data_parser = FeedDataParser()


def get_feed_data_parser() -> FeedDataParser:
    return feed_data_parser
