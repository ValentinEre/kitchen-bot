FROM python:3.11
WORKDIR /app
COPY ../requirements.txt ./
CMD["pwd"]
RUN pip install -r requirements.txt
RUN chmod 755 .
COPY .. .