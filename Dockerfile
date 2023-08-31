FROM python:3.11
# set work directory
WORKDIR /usr/src/bot/
# copy project
COPY . /usr/src/bot/
# install dependencies
RUN pip install --user aiogram, alembic, asyncpg, natasha, python-dotenv
# run app
CMD ["python", "bot.py"]