FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables will be passed at runtime
EXPOSE 8080

CMD ["python", "sm.py"]
