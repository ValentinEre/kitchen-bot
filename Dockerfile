FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y build-essential
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "bot"]