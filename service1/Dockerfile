FROM python:3.12-slim

WORKDIR /service

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "service.py"]