# Telegram-YT-Bot

Telegram bot that downloads YouTube videos from a given link.

Add your bot token and username tag to the environment variables in the dockerfile.

Run docker-compose up to start the bot.

After the image is built and running, you can test your Telegram bot.

It will try to download the best possible video+audio quality combination below the 50MiB size limit, if it is possible.
