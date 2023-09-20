FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt && apt-get install build-essential
COPY . .
CMD ["python", "-m", "bot"]