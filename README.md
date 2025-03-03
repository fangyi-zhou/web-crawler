# web-crawler

This is a Python implementation of the web crawler.

## Structure

Within the `web_crawler` directory, the project is laid out in the following way:

- `fetcher`: A package for implementing fetchers (for making HTTP requests),
    where the inferface is defined in `common.py`.
    Currently only an implementation using `aiohttp` is provided.
- `link_processor.py`: A module for processing HTML content to extract links in
    the contents. The module also handles relative URLs so ensure the returned
    results are absolute.
- `crawler.py`: A module for crawling web pages. The module uses the `asyncio`
    library to use asynchronous I/O with multiple workers to improve crawling
    efficiency.
- `__main__.py`: The main entry point to use the crawler as a CLI command.

## External Libraries

This implemetation uses the following external libraries (excluding dev dependencies):

- `beautifulsoup4`: A library for HTML parsing
- `aiohttp`: A library for making HTTP requests asynchronously
- `loguru`: A library for logging
- `tenacity`: A library for retrying
