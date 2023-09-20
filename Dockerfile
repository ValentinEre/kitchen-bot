FROM python:3.11
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get install build-essential
RUN pip install -r requirements.txt
COPY . /app