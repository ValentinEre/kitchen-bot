FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt && apt-get update && apt-get install -y build-essential
COPY . .
CMD ["python", "-m", "bot"]