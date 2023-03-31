import json
from datetime import datetime

import pytest

from tree_news.news_parser import parse_news_json


@pytest.mark.asyncio
async def test_parse_news_json_valid():
    json_string = json.dumps({
        "title": "Test Title",
        "body": "Test Body",
        "url": "https://example.com",
        "time": 1677649423000,
        "_id": "12345"
    })

    result = await parse_news_json(json_string)

    assert result == {
        "title": "Test Title",
        "body": "Test Body",
        "url": "https://example.com",
        "time": datetime.fromtimestamp(1677649423),
        "_id": "12345",
    }


@pytest.mark.asyncio
async def test_parse_news_json_invalid():
    json_string = "{Invalid JSON string}"

    with pytest.raises(json.JSONDecodeError):
        await parse_news_json(json_string)


@pytest.mark.asyncio
async def test_parse_news_json_missing_fields():
    json_string = json.dumps({
        "title": "Test Title",
        "body": "Test Body",
        "time": 1677649423000,
    })

    result = await parse_news_json(json_string)

    assert result == {
        "title": "Test Title",
        "body": "Test Body",
        "url": "",
        "time": datetime.fromtimestamp(1677649423),
        "_id": "",
    }
