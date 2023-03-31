"""
process_news.py

This module contains the process_news function, which is responsible for processing incoming
news updates from a websocket and sending them to a webhook.
"""

from typing import Dict

import aiohttp
from websockets.client import WebSocketClientProtocol

from .news_parser import parse_news_json
from .webhook_sender import send_to_webhook


async def process_news(
    websocket: WebSocketClientProtocol,
    session: aiohttp.ClientSession,
    webhook_url: str,
    latest_ping: Dict[WebSocketClientProtocol, int]
) -> None:
    """
    Process incoming news updates from a websocket and send them to a webhook.

    This function continuously listens for messages on the websocket, parses the received news
    updates, and sends them to the specified webhook URL. It ensures that only unique news updates
    are sent by maintaining a set of previously processed message IDs.

    Args:
        websocket (WebSocketClientProtocol): The connected websocket instance to receive news from.
        session (aiohttp.ClientSession): The aiohttp client session to send webhook requests.
        webhook_url (str): The URL of the webhook to send news updates to.
        latest_ping (Dict[WebSocketClientProtocol, int]): A dictionary of latest ping times 
                                                          for each websocket instance.

    Returns:
        None
    """
    unique_ids = set()

    while True:
        message = await websocket.recv()
        parsed_news = await parse_news_json(message)

        if parsed_news is not None:
            message_id = parsed_news["_id"]

            if message_id not in unique_ids:
                unique_ids.add(message_id)
                print(f"💌 Sending message {message_id} to webhook")
                if webhook_url:
                    await send_to_webhook(session, webhook_url, parsed_news, latest_ping[websocket])
            else:
                print(f"Duplicate message ignored: {message_id}")
