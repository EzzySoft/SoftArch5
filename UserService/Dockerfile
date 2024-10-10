FROM python:3.9-slim

WORKDIR /usr/local/app/user_service

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "user_service.py"]