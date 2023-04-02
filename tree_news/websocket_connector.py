"""
websocket_connector.py

This module provides a function to establish and maintain a connection to a websocket.
It handles reconnection attempts when the connection is lost or closed.
"""

from asyncio.exceptions import IncompleteReadError
from datetime import datetime

from websockets.client import connect
from websockets.exceptions import (ConnectionClosed, ConnectionClosedError,
                                   ConnectionClosedOK)

from .error_handler import handle_error


async def connect_to_websocket(websocket_uri: str):
    """
    Asynchronously connects to a websocket and yields the connection.

    This function will keep trying to connect to the specified websocket URI.
    If the connection is lost or closed, it will handle the error and attempt to reconnect.

    Args:
        websocket_uri (str): The URI of the websocket to connect to.

    Yields:
        WebSocketClientProtocol: The connected websocket instance.

    Raises:
        ConnectionClosedError: If the connection is closed with an unexpected status code.
        ConnectionClosedOK: If the connection is closed with a valid status code.
        ConnectionClosed: If the connection is closed for any reason.
    """
    while True:
        try:
            async with connect(websocket_uri) as websocket:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(
                    f'✅ Connected to websocket at {current_time}'
                )
                yield websocket
        except (
            ConnectionClosedError,
            ConnectionClosedOK,
            ConnectionClosed,
            IncompleteReadError
        ) as error:
            await handle_error(error)
