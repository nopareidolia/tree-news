"""
news_parser.py

This module contains the parse_news_json function, which parses a JSON string containing news
data and returns a dictionary with the extracted information.
"""

import json
from datetime import datetime
from typing import Dict, Optional, Union


async def parse_news_json(json_string: str) -> Optional[Dict[str, Union[str, datetime]]]:
    """
    Parses a JSON string containing news data and extracts relevant information.

    This function takes a JSON string as input, extracts the title, body, URL, timestamp,
    and ID of the news item, and returns a dictionary containing this information. If the
    JSON string cannot be parsed, the function raises a JSONDecodeError.

    Args:
        json_string (str): The JSON string to be parsed.

    Returns:
        Optional[Dict[str, Union[str, datetime]]]: A dictionary containing the parsed news data,
        or None if the JSON string could not be parsed.

    Raises:
        JSONDecodeError: If the JSON string cannot be parsed.
    """
    try:
        data = json.loads(json_string)

        title = data.get("title", "")
        body = data.get("body", "")
        url = data.get("url", "") or data.get("link", "")
        time = datetime.fromtimestamp(data.get("time", "") / 1000)
        _id = data.get("_id", "")

        return {
            "title": title,
            "body": body,
            "url": url,
            "time": time,
            "_id": _id,
        }
    except json.JSONDecodeError as exception:
        print(f"Error parsing JSON: {exception}")
        raise exception
