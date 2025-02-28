import argparse
import asyncio

from web_crawler.crawler import Crawler
from web_crawler.fetcher.aiohttp_fetcher import AiohttpFetcher


async def run_crawler(start_url: str):
    fetcher = AiohttpFetcher()
    crawler = Crawler(fetcher=fetcher)
    await crawler.start(start_url)


def main():
    parser = argparse.ArgumentParser(description="A simple web crawler")
    parser.add_argument("url", help="The URL to start the crawl from")
    args = parser.parse_args()
    asyncio.run(run_crawler(args.url))


main()
