from typing import Optional, Protocol


class Crawler(Protocol):
    """
    An interface for a crawler worker implementation
    """

    async def crawl(self, url: str) -> Optional[str]:
        """Fetch the requested URL, return the content when successful"""
        ...
