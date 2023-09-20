import os

from redis import Redis

redis = Redis(
    host=os.getenv("REDIS_HOST"),
    password=os.getenv("REDIS_PASSWORD"),
    port=os.getenv("REDIS_PORT"),
)
