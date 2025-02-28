from urllib.parse import urljoin

from bs4 import BeautifulSoup
from loguru import logger


def find_links(content: str, base_url: str) -> set[str]:
    """Find all the link in the HTML content. Links are returned as a set of
    strings, and any relative links are converted to absolute links.
    :param base_url: The base URL to use for relative links. Only used if no base tag is found in the HTML content.
    :param content: The HTML content to extract links from.
    :return: a set of strings of links found in the HTML content.
    """
    soup = BeautifulSoup(content, "html.parser")
    base_tag = soup.find("base")
    if base_tag:
        base_url = base_tag.attrs["href"]
        logger.debug("Found base url {} in HTML", base_url)
    return {
        urljoin(base_url, link.attrs["href"]) for link in soup.find_all("a", href=True)
    }
