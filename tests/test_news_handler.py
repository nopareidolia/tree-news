import unittest
from unittest.mock import AsyncMock, MagicMock

import pytest

from tree_news.news_handler import handle_news_json


@pytest.fixture
def mock_websocket_and_webhook():
    websocket = AsyncMock()
    webhook_url = "https://example.com/webhook"
    return websocket, webhook_url

class CustomAsyncIterator:
    def __init__(self, items):
        self.items = items

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.items:
            raise StopAsyncIteration
        return self.items.pop(0)

@pytest.mark.asyncio
async def test_handle_news_json(mock_websocket_and_webhook):
    websocket, webhook_url = mock_websocket_and_webhook

    # Mock connect_to_websocket to return the mock websocket
    connect_to_websocket_mock = MagicMock(return_value=CustomAsyncIterator([websocket]))

    # Mock update_ping to not raise any exception
    update_ping_mock = AsyncMock()

    # Mock exponential_backoff to not raise any exception
    exponential_backoff_mock = AsyncMock()

    with unittest.mock.patch("tree_news.news_handler.connect_to_websocket", connect_to_websocket_mock):
        with unittest.mock.patch("tree_news.news_handler.update_ping", update_ping_mock):
            with unittest.mock.patch("tree_news.news_handler.exponential_backoff", exponential_backoff_mock):
                await handle_news_json("wss://example.com/news", webhook_url)

    connect_to_websocket_mock.assert_called_once_with("wss://example.com/news")
    update_ping_mock.assert_called_once()
    exponential_backoff_mock.assert_called_once()
