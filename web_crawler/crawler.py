import asyncio
from typing import Optional

from loguru import logger

from web_crawler.fetcher.common import Fetcher
from web_crawler.link_processor import find_links

DEFAULT_WORKER_COUNT = 4


class Crawler:
    fetcher: Fetcher
    visited: set[str]
    worklist: asyncio.Queue
    start_url: str
    worker_count: int
    output: dict[str, set[str]]

    def __init__(
        self, fetcher: Fetcher, start_url: str, worker_count: Optional[int] = None
    ):
        self.fetcher = fetcher
        self.visited = set()
        self.worklist = asyncio.Queue()
        self.start_url = start_url
        self.worker_count = worker_count or DEFAULT_WORKER_COUNT
        self.output = dict()

    async def _process_url(self, url: str) -> None:
        """Process a single URL. Use the fetcher to fetch the content, and add
        new links into the worklist."""
        if url in self.visited:
            return
        self.visited.add(url)
        try:
            content = await self.fetcher.get_content(url)
        except:
            logger.exception("Failed to fetch URL {}", url)
            return
        if content is None:
            return
        all_links: set[str] = set(
            find_links(content, base_url=url),
        )
        self.output[url] = all_links
        logger.info("URL {} has following links {}", url, all_links)
        links_to_follow: set[str] = set(
            filter(lambda link: link.startswith(self.start_url), all_links)
        )
        new_urls = links_to_follow - self.visited
        await asyncio.gather(*(self.worklist.put(new_url) for new_url in new_urls))

    async def _worker(self, id: int) -> None:
        """Main loop for a worker task: continuous get new URLs to fetch and use
        the fetch to get the links."""
        logger.info("Starting worker task #{}", id)
        while True:
            url = await self.worklist.get()
            logger.debug("Worker id {} fetching {}", id, url)
            try:
                await self._process_url(url)
            finally:
                # Important: `task_done` needs to be called to signify to the queue
                # that processing has been done. Otherwise `.join` call would not
                # work properly.
                self.worklist.task_done()

    async def start(self) -> dict[str, set[str]]:
        """Start crawling."""
        await self.worklist.put(self.start_url)
        logger.info("Starting crawler with {} workers", self.worker_count)
        async with asyncio.TaskGroup() as group:
            tasks = [
                group.create_task(self._worker(i)) for i in range(self.worker_count)
            ]
            await self.worklist.join()
            # Cancel worker tasks since the all URLs in the worklist has been crawled.
            for task in tasks:
                task.cancel()
            logger.info("Done")
        return self.output
