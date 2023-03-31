"""
ping_updater.py

This module contains the update_ping function, which updates the ping time of a websocket
connection and stores the value in a dictionary.
"""
import asyncio
import time
from typing import Dict

from websockets.client import WebSocketClientProtocol

latest_ping: Dict[WebSocketClientProtocol, int] = {}

async def update_ping(
        websocket: WebSocketClientProtocol,
        ping_dict: Dict[WebSocketClientProtocol, int],
        interval: int = 10
    ) -> None:
    """
    Updates the ping time of a given websocket connection and stores it in the provided
    dictionary.

    This function sends a ping request to the websocket connection, waits for a response,
    and calculates the time taken for the round-trip. It then stores the half of the
    round-trip time in the provided dictionary as the latest ping time for the connection.
    The function continues to update the ping time at the specified interval.

    Args:
        websocket (WebSocketClientProtocol): The websocket connection to ping.
        ping_dict (Dict[WebSocketClientProtocol, int]): A dictionary containing the latest
            ping time for each websocket connection.
        interval (int): The interval between ping updates in seconds.

    Returns:
        None
    """
    while True:
        start_time = time.time()
        ping_waiter = await websocket.ping()
        await ping_waiter
        end_time = time.time()

        ping_dict[websocket] = int((end_time - start_time) * 1000 / 2)
        await asyncio.sleep(interval)
