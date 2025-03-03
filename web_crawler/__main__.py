import argparse
import asyncio
import json

from web_crawler.crawler import Crawler
from web_crawler.fetcher.aiohttp_fetcher import AiohttpFetcher


async def run_crawler(start_url: str) -> dict[str, list[str]]:
    fetcher = AiohttpFetcher()
    crawler = Crawler(fetcher=fetcher, start_url=start_url)
    results = await crawler.start()
    # Convert set to list for JSON serialization
    return {url: sorted(list(links)) for url, links in results.items()}


def main():
    parser = argparse.ArgumentParser(description="A simple web crawler")
    parser.add_argument("url", help="The URL to start the crawl from")
    args = parser.parse_args()
    results = asyncio.run(run_crawler(args.url))
    print(json.dumps(results, indent=2))


main()
