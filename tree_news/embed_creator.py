"""
embed_creator.py

This module contains the create_embed function, which generates a Discord Embed object based on
provided news data. The function determines the embed's appearance, such as its color and author,
depending on the news source's domain.
"""

from datetime import datetime
from typing import Dict, Union
from urllib.parse import urlparse
from discord import Colour, Embed

def create_embed(data: Dict[str, Union[str, datetime]], latest_ping: int) -> Embed:
    """
    Create a Discord Embed object based on the provided news data.

    The appearance of the Embed object is determined by the news source's domain. For example,
    if the domain is "twitter.com", the embed will have a blue color, and the author will be
    the tweet's author. For other domains, the embed will have a fuchsia color, and the author
    will be the domain itself.

    Args:
        data (Dict[str, Union[str, datetime]]): A dictionary containing the news data, including
            the title, body, URL, and timestamp.
        latest_ping (int): The latest ping in milliseconds.

    Returns:
        Embed: A Discord Embed object containing the news data, with attributes set according
            to the news source's domain.
    """

    domain = urlparse(data["url"]).netloc

    # Set the description, author name, and color of the embed based on the news source
    if domain == "twitter.com":
        description = data["body"]
        author_name = data["title"]
        color = Colour.blue()
    else:
        description = data["title"]
        author_name = domain
        color = Colour.fuchsia()

    # Create an embed object and set its attributes
    embed = Embed(colour=color, description=description, timestamp=data["time"])
    embed.set_author(name=author_name, url=data["url"])
    embed.set_footer(text=f"🌲 Tree News | Ping: {latest_ping} ms")

    return embed
