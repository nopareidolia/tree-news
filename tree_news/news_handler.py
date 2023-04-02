"""
news_handler.py

This module contains the main function for asynchronously handling news updates.
It connects to a news websocket, processes incoming news updates, and sends them 
to a webhook if provided.
"""

import asyncio
import logging
from typing import Optional

import aiohttp

from .error_handler import handle_error
from .ping_updater import latest_ping, update_ping
from .process_news import process_news
from .retry import exponential_backoff
from .websocket_connector import connect_to_websocket

logger = logging.getLogger(__name__)


async def handle_news_json(
        websocket_uri: str,
        webhook_url: Optional[str] = None
    ) -> None:
    """
    Connects to the news websocket, processes news updates, and sends them to a webhook if provided.

    This function establishes a connection to the specified news websocket, 
    listens for incoming news updates, processes them using the process_news function, 
    and sends the processed updates to the specified webhook URL if provided. 
    It also handles reconnection attempts in case of connection loss or closure.

    Args:
        websocket_uri (str): The URI of the news websocket to connect to.
        webhook_url (Optional[str]): The webhook URL to send processed news updates to. 
                                     If None, no updates are sent.

    """
    async with aiohttp.ClientSession() as session:
        async for websocket in connect_to_websocket(websocket_uri):
            update_ping_task = asyncio.create_task(update_ping(websocket, latest_ping))

            try:
                await exponential_backoff(
                    5,
                    process_news,
                    websocket,
                    session,
                    webhook_url,
                    latest_ping
                )
            except Exception as exception:
                # Handle the error using the handle_error function
                await handle_error(exception)

            update_ping_task.cancel()

