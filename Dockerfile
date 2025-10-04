FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY src src/
COPY image image/
COPY .env .env

CMD ["python", "main.py"]