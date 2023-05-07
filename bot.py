import os
import re

import validators
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
BOT_USERNAME = os.environ.get('TELEGRAM_BOT_USERNAME')

# Check if environment variables are set
if TOKEN is None:
    print('Error: TELEGRAM_BOT_TOKEN environment variable not set')
    exit(1)

if BOT_USERNAME is None:
    print('Error: TELEGRAM_BOT_USERNAME environment variable not set')
    exit(1)


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me! I am a Python Telegram bot!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send me a URL link that contains a video!')


# Responses
def handle_response(text: str) -> str:
    if not validators.url(text):
        return 'Not a valid URL link!'

    ydl_opts = {"outtmpl": "%(id)s.%(ext)s",
                "format":
                    "bestvideo[filesize<40M][ext=mp4]+bestaudio[filesize<10M][ext=m4a]"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(text, download=True)
            video_id = info.get("id", "video")
            ext = info.get("ext", "video")
        except yt_dlp.DownloadError:
            return 'Failed to download video!'

    return f"{video_id}.{ext}"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Group chat or private chat?
    message_type: str = update.message.chat.type

    # Message we can process
    text: str = update.message.text

    # User who sent the message - with the message logged
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        # only respond if bot is tagged
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    if not re.match(".*mp4", response):
        await update.message.reply_text(text=response)
    else:
        await update.message.reply_document(document=open(response, 'rb'))
        os.remove(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.error)
    await update.message.reply_text("An unknown error happened!")


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Check for new messages every three seconds
    print('Polling...')
    app.run_polling(poll_interval=3)
