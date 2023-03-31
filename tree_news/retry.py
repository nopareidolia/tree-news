"""
retry.py

This module contains the exponential_backoff function, which implements an exponential backoff
retry mechanism for executing a given async function. If the function raises an exception, it
will be retried up to a specified number of times with an exponentially increasing delay between
attempts.
"""

import asyncio
from typing import Any, Callable, TypeVar

T = TypeVar("T", bound=Callable[..., Any])

async def exponential_backoff(retries: int, func: T, *args: Any, **kwargs: Any) -> Any:
    """
    Executes the given async function with an exponential backoff retry mechanism.

    If the function raises an exception, it will be retried up to 'retries' number of times,
    with an exponentially increasing delay between attempts. The initial delay is one second,
    and it doubles after each failed attempt.

    Args:
        retries (int): The number of retries before giving up.
        func (Callable): The async function to execute with retries.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        Any: The result of the function execution.

    Raises:
        Exception: If the function fails to execute successfully after all the retries.
    """

    delay = 1  # Initial delay in seconds

    for attempt in range(retries):
        try:
            return await func(*args, **kwargs)
        except Exception as exception:
            if attempt + 1 == retries:
                raise exception

            wait_time = delay * (2 ** attempt)
            await asyncio.sleep(wait_time)
