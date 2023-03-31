"""
webhook_sender.py

This module contains the send_to_webhook function responsible for sending data to a Discord webhook.
It uses the aiohttp library for sending HTTP requests and the Discord.py library for creating
Embed objects to be sent via the webhook.
"""

from datetime import datetime
from typing import Dict, Union

import aiohttp
from discord import Webhook

from .embed_creator import create_embed


async def send_to_webhook(
        session: aiohttp.ClientSession,
        webhook_url: str, data: Dict[str, Union[str, datetime]],
        latest_ping: int
    ) -> None:
    """
    Send data to a Discord webhook as an embed.

    This function creates a Discord Embed object from the provided data using 
    the create_embed function, then sends the embed to the specified Discord 
    webhook using the aiohttp.ClientSession.

    Args:
        session (aiohttp.ClientSession): The aiohttp ClientSession to use for sending 
                                         the webhook request.
        webhook_url (str): The URL of the Discord webhook.
        data (Dict[str, Union[str, datetime]]): A dictionary containing the news data 
                                                to be sent as an embed.
        latest_ping (int): The latest ping in milliseconds.

    Returns:
        None
    """
    # Create a Discord Webhook object
    webhook = Webhook.from_url(webhook_url, session=session)

    # Create an embed object
    embed = create_embed(data, latest_ping)

    # Send the embed to the webhook
    await webhook.send(embed=embed, username='🌲 Tree News')
