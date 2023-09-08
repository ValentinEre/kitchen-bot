FROM python:3.11
WORKDIR /app
COPY . /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN chmod 755 .
COPY . .