import asyncio

from aiohttp import ClientSession

from web_crawler.fetcher.aiohttp_fetcher import AiohttpFetcher
from web_crawler.link_processor import find_links


async def test():
    session = ClientSession()
    fetcher = AiohttpFetcher(session=session)
    url = "https://example.com/"
    content = await fetcher.get_content(url)
    links = find_links(content, base_url=url)
    print(links)


asyncio.run(test())
