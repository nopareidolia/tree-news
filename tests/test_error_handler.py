import io
import logging
import unittest.mock
from unittest.mock import AsyncMock

import pytest

from tree_news.error_handler import handle_error


@pytest.mark.asyncio
async def test_handle_error():
    # Create a custom logger and handler to capture log messages
    log_capture = io.StringIO()
    custom_handler = logging.StreamHandler(log_capture)
    custom_handler.setLevel(logging.ERROR)
    custom_logger = logging.getLogger("test_logger")
    custom_logger.addHandler(custom_handler)
    custom_logger.setLevel(logging.ERROR)

    # Mock asyncio.sleep to avoid waiting during the test
    sleep_mock = AsyncMock()
    with unittest.mock.patch("asyncio.sleep", sleep_mock):
        with unittest.mock.patch("tree_news.error_handler.logger", custom_logger):
            test_exception = ValueError("Test exception message")
            await handle_error(test_exception)

    # Check if the error message is logged correctly
    log_output = log_capture.getvalue()
    assert "Test exception message" in log_output
    assert "Error at" in log_output

    # Verify that asyncio.sleep was called once with the default delay (5 seconds)
    sleep_mock.assert_called_once_with(5)
