from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ClientSession
from discord import Webhook

from tree_news.webhook_sender import send_to_webhook


@pytest.mark.asyncio
async def test_send_to_webhook():
    # Create a sample webhook URL and data
    webhook_url = "https://fake.webhook.url"
    data = {
        "title": "Sample Title",
        "description": "Sample Description",
        "timestamp": "2023-04-01 00:00:00",
    }
    latest_ping = 100

    # Mock the Webhook.from_url and Webhook.send methods
    with patch("tree_news.webhook_sender.Webhook.from_url", new_callable=MagicMock) as mock_from_url, \
            patch("tree_news.webhook_sender.create_embed", new_callable=MagicMock) as mock_create_embed:

        # Create a mock Webhook instance and set up the send method as an AsyncMock
        mock_webhook = MagicMock(spec=Webhook)
        mock_webhook.send = AsyncMock()
        mock_from_url.return_value = mock_webhook

        # Create a mock Embed object
        mock_embed = MagicMock()
        mock_create_embed.return_value = mock_embed

        # Create a mock aiohttp ClientSession
        session = MagicMock(spec=ClientSession)

        # Call the send_to_webhook function
        await send_to_webhook(session, webhook_url, data, latest_ping)

        # Check that the from_url method was called with the correct arguments
        mock_from_url.assert_called_once_with(webhook_url, session=session)

        # Check that the create_embed method was called with the correct arguments
        mock_create_embed.assert_called_once_with(data, latest_ping)

        # Check that the send method was called with the correct arguments
        mock_webhook.send.assert_called_once_with(embed=mock_embed, username='🌲 Tree News')
