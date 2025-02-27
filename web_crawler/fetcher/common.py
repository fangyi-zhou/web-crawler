from typing import Optional, Protocol


class Fetcher(Protocol):
    """
    An interface for a crawler worker implementation
    """

    async def get_content(self, url: str) -> Optional[str]:
        """Fetch the requested URL, return the content when successful"""
        ...
