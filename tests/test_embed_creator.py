import datetime

from discord import Colour

from tree_news.embed_creator import create_embed


def test_create_embed_twitter():
    # Example data from a Twitter source
    twitter_data = {
        "title": "Twitter Author",
        "body": "Tweet content",
        "url": "https://twitter.com/user/status/1234567890",
        "time": datetime.datetime.now(),
    }
    latest_ping = 100

    # Create embed object
    embed = create_embed(twitter_data, latest_ping)

    # Check if attributes are correctly set for a Twitter source
    assert embed.colour == Colour.blue()
    assert embed.description == twitter_data["body"]
    assert embed.author.name == twitter_data["title"]
    assert embed.author.url == twitter_data["url"]
    assert embed.footer.text.startswith("🌲 Tree News")

def test_create_embed_other():
    # Example data from a non-Twitter source
    other_data = {
        "title": "News Title",
        "body": "News content",
        "url": "https://example.com/news/1234567890",
        "time": datetime.datetime.now(),
    }
    latest_ping = 100

    # Create embed object
    embed = create_embed(other_data, latest_ping)

    # Check if attributes are correctly set for a non-Twitter source
    assert embed.colour == Colour.fuchsia()
    assert embed.description == other_data["title"]
    assert embed.author.name == "example.com"
    assert embed.author.url == other_data["url"]
    assert embed.footer.text.startswith("🌲 Tree News")
