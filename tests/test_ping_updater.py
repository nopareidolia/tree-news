import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from websockets.client import WebSocketClientProtocol

from tree_news.ping_updater import update_ping, latest_ping


@pytest.mark.asyncio
async def test_update_ping():
    # Mock the websocket
    websocket = MagicMock(spec=WebSocketClientProtocol)
    websocket.ping.return_value = asyncio.Future()
    websocket.ping.return_value.set_result(None)

    # Mock the time.time() function
    with patch("tree_news.ping_updater.time.time") as mock_time:
        mock_time.side_effect = [1.0, 1.2, 2.0, 2.2, 3.0, 3.2]

        # Call the update_ping function with the mocks and a short interval
        update_task = asyncio.create_task(update_ping(websocket, latest_ping, interval=0.1))

        # Wait for a short while to let the function update the ping a few times
        await asyncio.sleep(0.4)

        # Cancel the update_ping task
        update_task.cancel()

        # Check if the ping was updated correctly
        assert latest_ping[websocket] == 100
        assert websocket.ping.call_count == 3
