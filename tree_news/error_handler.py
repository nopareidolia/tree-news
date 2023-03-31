"""
Error handler for the tree_news package.
"""

import asyncio
from datetime import datetime
from typing import Type
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_error(exception: Type[Exception], delay: int = 5) -> None:
    """Handle an error by logging it and waiting for a certain delay.

    Args:
        exception (Type[Exception]): The exception to be handled.
        delay (int, optional): The delay in seconds. Defaults to 5.

    Returns:
        None
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.error("Error at %s: %s", current_time, exception)
    await asyncio.sleep(delay)
