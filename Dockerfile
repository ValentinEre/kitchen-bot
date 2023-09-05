FROM python:3.11
WORKDIR /bot/
COPY . /bot/
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python bot.py"]