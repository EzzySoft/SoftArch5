FROM python:3.9-slim

WORKDIR /usr/local/app/feed_service

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5004

CMD ["python", "feed_service.py"]