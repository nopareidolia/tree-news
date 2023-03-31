from asyncio import TimeoutError
from unittest.mock import AsyncMock

import pytest

from tree_news.retry import exponential_backoff


@pytest.mark.asyncio
async def test_exponential_backoff_success():
    # Mock an async function that returns a value without raising an exception
    mock_async_func = AsyncMock(return_value="success")

    # Call the exponential_backoff function
    result = await exponential_backoff(3, mock_async_func, "arg1", "arg2", kwarg1="value1")

    # Check that the mock_async_func was called with the correct arguments
    mock_async_func.assert_called_once_with("arg1", "arg2", kwarg1="value1")

    # Check that the result is as expected
    assert result == "success"


@pytest.mark.asyncio
async def test_exponential_backoff_failure():
    # Mock an async function that raises a TimeoutError
    mock_async_func = AsyncMock(side_effect=TimeoutError)

    # Call the exponential_backoff function and expect it to raise a TimeoutError
    with pytest.raises(TimeoutError):
        await exponential_backoff(3, mock_async_func, "arg1", "arg2", kwarg1="value1")

    # Check that the mock_async_func was called 3 times with the correct arguments
    assert mock_async_func.call_count == 3
    mock_async_func.assert_called_with("arg1", "arg2", kwarg1="value1")
