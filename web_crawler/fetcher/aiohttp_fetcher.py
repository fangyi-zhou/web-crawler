from typing import Optional

from aiohttp import ClientSession
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

CONTENT_TYPE_HTML = "text/html"
STATUS_OK = 200


class AiohttpFetcher:
    """A crawler implementation that uses aiohttp for asynchronous crawling"""

    @retry(wait=wait_exponential_jitter(max=30), stop=stop_after_attempt(5))
    async def get_content(self, url: str) -> Optional[str]:
        async with ClientSession() as session:
            async with session.get(
                url, headers={"Accept": CONTENT_TYPE_HTML}
            ) as response:
                if response.status != 200:
                    logger.warning(
                        "Got non-OK status {}, skipping. url = {}", response.status, url
                    )
                    return None
                # Check the content type in header. If none is present, let's assume the content is html.
                if CONTENT_TYPE_HTML not in response.headers.get(
                    "Content-Type", CONTENT_TYPE_HTML
                ):
                    logger.warning(
                        "Got non-HTML content type {}, skipping. url = {}",
                        response.headers.get("Content-Type"),
                        url,
                    )
                    return None
                try:
                    return await response.text()
                except UnicodeDecodeError:
                    logger.exception("Failed to decode response as text")
                    return None
