FROM python:3.9-slim

WORKDIR /usr/local/app/like_service

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["python", "like_service.py"]