import asyncio

from aiohttp import ClientSession

from web_crawler.crawling.crawling_worker_aiohttp import AiohttpCrawler
from web_crawler.link_processor import find_links


async def test():
    session = ClientSession()
    crawler = AiohttpCrawler(session=session)
    url = "https://example.com/"
    content = await crawler.get_content(url)
    links = find_links(content, base_url=url)
    print(links)


asyncio.run(test())
