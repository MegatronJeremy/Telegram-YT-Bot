FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y ffmpeg && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
