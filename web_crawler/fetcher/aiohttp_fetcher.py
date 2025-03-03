from typing import Optional

from aiohttp import ClientSession
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

CONTENT_TYPE_HTML = "text/html"
STATUS_OK = 200

DEFAULT_MAX_WAIT_TIME_IN_SECONDS = 30
DEFAULT_MAX_RETRY_ATTEMPTS = 5


class AiohttpFetcher:
    """A crawler implementation that uses aiohttp for asynchronous crawling"""

    @retry(
        wait=wait_exponential_jitter(max=DEFAULT_MAX_WAIT_TIME_IN_SECONDS),
        stop=stop_after_attempt(DEFAULT_MAX_RETRY_ATTEMPTS),
    )
    async def get_content(self, url: str) -> Optional[str]:
        async with ClientSession() as session:
            async with session.get(
                url, headers={"Accept": CONTENT_TYPE_HTML}
            ) as response:
                if response.status != STATUS_OK:
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
