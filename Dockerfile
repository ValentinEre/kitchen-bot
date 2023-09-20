FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get install build-essential
RUN pip install -r requirements.txt
COPY . /app
CMD ["python", "-m", "bot"]