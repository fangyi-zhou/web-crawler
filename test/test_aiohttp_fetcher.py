from unittest.mock import AsyncMock, MagicMock

import pytest

from web_crawler.fetcher.aiohttp_fetcher import AiohttpFetcher, ClientSession


@pytest.fixture
def mock_request(mocker):
    # This should be a async context manager
    mock_request = MagicMock()
    mock_request.return_value.__aenter__ = AsyncMock()
    mock_request.return_value.__aexit__ = AsyncMock()

    mocker.patch.object(ClientSession, "get", mock_request)

    return mock_request.return_value.__aenter__


async def test_fetcher_returns_response_text(mock_request):
    mock_request.return_value.status = 200
    mock_request.return_value.headers = {"Content-Type": "text/html"}
    mock_request.return_value.text = AsyncMock(return_value="It works")
    fetcher = AiohttpFetcher()
    content = await fetcher.get_content("foo")
    assert content == "It works"


async def test_fetcher_returns_none_for_non_200(mock_request):
    mock_request.return_value.status = 404
    fetcher = AiohttpFetcher()
    content = await fetcher.get_content("foo")
    assert content is None


async def test_fetcher_returns_none_for_non_html_content_type(mock_request):
    mock_request.return_value.status = 200
    mock_request.return_value.headers = {"Content-Type": "application/json"}
    fetcher = AiohttpFetcher()
    content = await fetcher.get_content("foo")
    assert content is None


async def test_fetcher_returns_content_for_empty_content_type(mock_request):
    mock_request.return_value.status = 200
    mock_request.return_value.headers = {}
    mock_request.return_value.text = AsyncMock(return_value="It works")
    fetcher = AiohttpFetcher()
    content = await fetcher.get_content("foo")
    assert content == "It works"


async def test_fetcher_returns_none_for_binary_response(mock_request):
    mock_request.return_value.status = 200
    mock_request.return_value.headers = {"Content-Type": "text/html"}
    # When decoding binary as utf8, a UnicodeDecodeError will be raised
    mock_request.return_value.text = AsyncMock(
        side_effect=UnicodeDecodeError("", bytes([]), 0, 0, "")
    )
    fetcher = AiohttpFetcher()
    content = await fetcher.get_content("foo")
    assert content is None
