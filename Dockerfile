FROM python:3.11
# set work directory
WORKDIR /bot/
# copy project
COPY . /bot/
# install dependencies
RUN pip install --user aiogram, alembic, asyncpg, natasha, python-dotenv
# run app
CMD ["python", "bot.py"]