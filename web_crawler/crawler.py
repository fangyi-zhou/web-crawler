from loguru import logger

from web_crawler.fetcher.common import Fetcher
from web_crawler.link_processor import find_links


class Crawler:
    fetcher: Fetcher
    visited: set[str]

    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher
        self.visited = set()

    async def start(self, start_url: str) -> None:
        worklist: list[str] = [start_url]
        while worklist:
            url = worklist.pop()
            if url in self.visited:
                continue
            self.visited.add(url)
            try:
                content = await self.fetcher.get_content(url)
            except:
                logger.exception("Failed to fetch URL {}", url)
                continue
            if content is None:
                continue
            links: set[str] = set(
                filter(
                    lambda link: link.startswith(start_url),
                    find_links(content, base_url=url),
                )
            )
            logger.info("URL {} has following links {}", url, links)
            worklist.extend(links - self.visited)
