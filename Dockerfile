FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV BOT_TOKEN=your_bot_token_here
EXPOSE 8080

CMD ["python", "sm.py"]
