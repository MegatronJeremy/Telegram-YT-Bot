FROM python:3.10

# Set environment variables
ENV TELEGRAM_BOT_TOKEN your_token_here
ENV TELEGRAM_BOT_USERNAME your_bot_username_here

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y ffmpeg && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
