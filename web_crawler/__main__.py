import asyncio

from web_crawler.crawler import Crawler
from web_crawler.fetcher.aiohttp_fetcher import AiohttpFetcher


async def test():
    fetcher = AiohttpFetcher()
    crawler = Crawler(fetcher=fetcher)
    url = "https://example.com/"
    await crawler.start(url)


asyncio.run(test())
