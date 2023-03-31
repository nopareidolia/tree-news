from unittest.mock import MagicMock, patch

import pytest
from aiohttp import ClientSession
from websockets.client import WebSocketClientProtocol

from tree_news.process_news import process_news


class TestException(Exception):
    pass


@pytest.mark.asyncio
async def test_process_news():
    # Mock the websocket
    websocket = MagicMock(spec=WebSocketClientProtocol)
    websocket.recv.side_effect = ["message1", "message2", "message3", TestException()]

    # Mock the parse_news_json function
    with patch("tree_news.process_news.parse_news_json") as mock_parse_news_json:
        mock_parse_news_json.side_effect = [
            {"_id": "msg1"},
            {"_id": "msg2"},
            {"_id": "msg3"},
        ]

        # Mock the send_to_webhook function
        with patch("tree_news.process_news.send_to_webhook") as mock_send_to_webhook:
            # Mock the aiohttp client session
            session = MagicMock(spec=ClientSession)

            webhook_url = "http://example.com/webhook"

            # Mock the latest_ping dictionary
            latest_ping = {websocket: 1000}

            with pytest.raises(TestException):
                # Call the process_news function with the mocks
                await process_news(
                    websocket,
                    session,
                    webhook_url,
                    latest_ping
                )

    # Check that the websocket.recv function was called 4 times
    assert websocket.recv.call_count == 4

    # Check that the send_to_webhook function was called 3 times with the correct arguments
    assert mock_send_to_webhook.call_count == 3
    mock_send_to_webhook.assert_called_with(
        session, webhook_url, {"_id": "msg3"}, 1000
    )
