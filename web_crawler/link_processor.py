from urllib.parse import urldefrag, urljoin

from bs4 import BeautifulSoup
from loguru import logger


def _process_link(link: str, base_url: str) -> str:
    """Process a single link, converting relative links to absolute links, and also removing any fragments.
    :param link: The link to process.
    :param base_url: The base URL to use for relative links.
    :return: The processed link.
    """
    link = urljoin(base_url, link)
    url, _fragment = urldefrag(link)
    return url


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
        _process_link(link.attrs["href"], base_url=base_url)
        for link in soup.find_all("a", href=True)
    }
