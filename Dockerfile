FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get install make
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "bot"]