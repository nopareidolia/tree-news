# Tree News
![pylint](https://github.com/nopareidolia/tree-news/actions/workflows/pylint.yml/badge.svg)
![coverage](https://github.com/nopareidolia/tree-news/actions/workflows/coverage.yml/badge.svg)
![pytest](https://github.com/nopareidolia/tree-news/actions/workflows/pytest.yml/badge.svg)
![docker](https://github.com/nopareidolia/tree-news/actions/workflows/docker-image.yml/badge.svg)


Tree News is a Python application that fetches the latest news from Tree of Alpha and sends it to a Discord webhook.

## Overview
Tree News fetches the latest news from the Tree of Alpha API and sends it to a Discord webhook. It uses asyncio to handle incoming messages from the API and sends them to the webhook using the requests library.

## Installation
To install Tree News, first clone the repository:

```py
git clone https://github.com/nopareidolia/tree-news.git
```

Then install the dependencies using Poetry:

```py
cd tree-news
poetry install
```

## Usage
To use Tree News, first set the `WEBHOOK_URL` environment variable to the URL of your Discord webhook:

```py
export WEBHOOK_URL=https://discord.com/api/webhooks/1234567890
```

Then run the `tree-news` command:

```py
poetry run python -m tree_news
```

Tree News will start fetching news from the Tree of Alpha API and sending it to the webhook.

## Configuration
Tree News does not require any additional configuration beyond setting the `WEBHOOK_URL` environment variable.

## Obtaining a Discord Webhook URL for a Channel

Follow these steps to create a webhook URL for a specific channel in your Discord server:

1. Open the Discord app and navigate to the server where you want to create a webhook.

2. Right-click on the desired channel and select **Edit Channel**.

3. In the channel settings, click on the **Integrations** tab.

4. Click on the **Create Webhook** button. If there are existing webhooks, click on the **View Webhooks** button and then click **New Webhook**.

5. Customize the webhook settings, such as the name and profile picture (optional).

6. Copy the **Webhook URL** by clicking on the **Copy Webhook URL** button. This URL will be used to send messages to the channel.

7. Click **Save** to create the webhook.

Keep the webhook URL private, as anyone with the URL can use it to send messages to your channel. To update or delete the webhook, return to the **Integrations** tab in the channel settings.

## Installation and Running with Docker (Recommended)
Follow these steps to run the Tree News application using Docker:

1. Make sure you have Docker and Docker Compose installed on your system. If you don't have them installed, follow the instructions in the official Docker documentation and Docker Compose documentation to set them up.

2. Create a new directory for your docker-compose.yml file:
```bash
mkdir tree-news-docker
cd tree-news-docker
```

3. Create a docker-compose.yml file with the following content:
```yml
version: '1'
services:
  tree-news:
    image: nopareidolia/tree-news:latest
    restart: unless-stopped
    environment:
      - WEBHOOK_URL=<your_webhook_url>
```

Replace <your_webhook_url> with the actual value for your webhook URL.

4. Run the Tree News application using Docker Compose:
```bash
docker-compose up
```

This command will start the Tree News application in the background. To stop the application, press Ctrl+C or run docker-compose down.

5. That's it! The Tree News application should now be running on your system.

## Contributing
If you find a bug or would like to contribute to Tree News, please open an issue or submit a pull request on GitHub.

## License
Tree News is released under the MIT License.

