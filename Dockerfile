FROM python:3.11-slim-buster

RUN apt-get update && apt-get install -y ffmpeg git

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
