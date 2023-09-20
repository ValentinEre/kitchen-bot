FROM python:3.11
WORKDIR /app
COPY requirements.txt ./app
RUN pip install -r ./app/requirements.txt && chmod 755 .
COPY . .
CMD ["python", "-m", "bot"]