"""
Main entry point for the application.
"""

import asyncio
import os

from .news_handler import handle_news_json

async def main():
    """
    Main entry point for the application.
    """
    websocket_uri = "wss://news.treeofalpha.com/ws"
    webhook_url = os.getenv(
        "WEBHOOK_URL",
        ""
    )
    await handle_news_json(websocket_uri, webhook_url=webhook_url)

if __name__ == "__main__":
    asyncio.run(main())
