FROM python:3.11
WORKDIR /app
COPY ../requirements.txt ./
RUN pip install -r requirements.txt && chmod 755 .
COPY .. .
CMD ["python", "-m", "bot"]