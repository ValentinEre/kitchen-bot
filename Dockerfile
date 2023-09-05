FROM python:3.11
# set work directory
WORKDIR /bot/
# copy project
COPY . /bot/
# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
# run app
CMD ["python", "bot.py"]