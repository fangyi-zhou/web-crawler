import asyncio

from aiohttp import ClientSession

from web_crawler.crawler import Crawler
from web_crawler.fetcher.aiohttp_fetcher import AiohttpFetcher
from web_crawler.link_processor import find_links


async def test():
    session = ClientSession()
    fetcher = AiohttpFetcher(session=session)
    crawler = Crawler(fetcher=fetcher)
    url = "https://example.com/"
    await crawler.start(url)


asyncio.run(test())
