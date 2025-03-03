from typing import Optional

from web_crawler.crawler import Crawler

MOCK_EXAMPLE_HTML = """
<html>
<body>
    <a href="https://other-domain.com">Other Domain</a>
    <a href="https://different.example.com">Other Subdomain</a>
    <a href="https://example.com/about">Should follow</a>
</body>
</html>
"""


class MockFetcher:
    async def get_content(self, url: str) -> Optional[str]:
        if url == "https://example.com":
            return MOCK_EXAMPLE_HTML
        if url == "https://example.com/none":
            return None
        if url == "https://example.com/throws":
            raise RuntimeError()


async def test_crawler_process_url_follows_links_correctly():
    fetcher = MockFetcher()
    crawler = Crawler(fetcher=fetcher, start_url="https://example.com", worker_count=1)
    await crawler._process_url("https://example.com")
    assert crawler.worklist.qsize() == 1
    # Only 1 link should be added, which is the one that matched the domain
    assert await crawler.worklist.get() == "https://example.com/about"
    links = crawler.output["https://example.com"]
    assert len(links) == 3
    assert "https://other-domain.com" in links
    assert "https://different.example.com" in links
    assert "https://example.com/about" in links


async def test_crawler_process_url_skips_visited():
    fetcher = MockFetcher()
    crawler = Crawler(fetcher=fetcher, start_url="https://example.com", worker_count=1)
    crawler.visited.add("https://example.com")
    await crawler._process_url("https://example.com")
    # No new links should be added since the link has already been visited
    assert crawler.worklist.qsize() == 0


async def test_crawler_process_url_handles_empty_response_from_fetcher():
    fetcher = MockFetcher()
    crawler = Crawler(fetcher=fetcher, start_url="https://example.com", worker_count=1)
    await crawler._process_url("https://example.com/none")
    # No new links should be added since the link doesn't reach anywhere
    assert crawler.worklist.qsize() == 0
    # No output entry since fetching did not succeed
    assert "https://example.com/none" not in crawler.output


async def test_crawler_process_url_handles_exception_from_fetcher():
    fetcher = MockFetcher()
    crawler = Crawler(fetcher=fetcher, start_url="https://example.com", worker_count=1)
    await crawler._process_url("https://example.com/throws")
    # No new links should be added since an error occurs during fetching
    assert crawler.worklist.qsize() == 0
    # No output entry since fetching did not succeed
    assert "https://example.com/throws" not in crawler.output
