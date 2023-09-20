import os

from redis import Redis

redis = Redis(
    host=os.getenv("REDIS_HOST"),
    db=os.getenv("REDIS_DB"),
    password=os.getenv("REDIS_PASSWORD")
)
