from unittest.mock import MagicMock, patch

import pytest
from websockets.exceptions import ConnectionClosedOK

from tree_news.websocket_connector import connect_to_websocket


class AsyncContextManagerMock:
    def __init__(self, enter_result=None, side_effect=None):
        self.enter_result = enter_result
        self.side_effect = side_effect

    async def __aenter__(self):
        if self.side_effect:
            raise self.side_effect
        return self.enter_result

    async def __aexit__(self, exc_type, exc_value, traceback):
        return False

@pytest.mark.asyncio
async def test_connect_to_websocket_success():
    # Mock the `connect` function to simulate a successful connection
    mock_websocket = MagicMock()
    with patch("tree_news.websocket_connector.connect") as mock_connect:
        mock_connect.return_value = AsyncContextManagerMock(enter_result=mock_websocket)
        
        # Run the test
        async for _ in connect_to_websocket("ws://fake.uri"):
            break

@pytest.mark.asyncio
async def test_connect_to_websocket_reconnect_on_closed_connection():
    # Mock the `connect` function to simulate a closed connection followed by a successful connection
    mock_websocket = MagicMock()
    connection_closed_ok_instance = ConnectionClosedOK(1000, 1000, rcvd_then_sent=1000)
    with patch("tree_news.websocket_connector.connect") as mock_connect:
        mock_connect.side_effect = [
            AsyncContextManagerMock(side_effect=connection_closed_ok_instance),
            AsyncContextManagerMock(enter_result=mock_websocket),
        ]

        # Run the test
        async for _ in connect_to_websocket("ws://fake.uri"):
            break
