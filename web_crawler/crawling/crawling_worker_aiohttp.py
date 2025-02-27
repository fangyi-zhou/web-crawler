from typing import Optional

from aiohttp import ClientSession
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

CONTENT_TYPE_HTML = "text/html"
STATUS_OK = 200


class AiohttpCrawler:
    """A crawler implementation that uses aiohttp for asynchronous crawling"""

    session: ClientSession

    def __init__(self, session: ClientSession):
        self.session = session

    @retry(wait=wait_exponential_jitter(max=30), stop=stop_after_attempt(5))
    async def get_content(self, url: str) -> Optional[str]:
        async with self.session as session:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.warning(
                        "Got non-OK status {}, skipping. url = {}", response.status, url
                    )
                    return None
                # FIXME: Check for content type and bail out early
                return await response.text()
