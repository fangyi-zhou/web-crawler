import pytest

from web_crawler.crawler import Crawler
from web_crawler.fetcher.aiohttp_fetcher import AiohttpFetcher


@pytest.mark.integ
async def test_integration_test():
    fetcher = AiohttpFetcher()
    start_url = "https://fangyi.io"
    crawler = Crawler(fetcher=fetcher, start_url=start_url)
    result = await crawler.start()
    assert len(result) > 0
    for links in result:
        assert len(links) > 0
