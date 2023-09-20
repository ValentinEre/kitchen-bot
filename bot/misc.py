import os

from redis.asyncio import Redis

redis = Redis(
    host=os.getenv("REDIS_HOST"),
    port=6378,
    db=os.getenv("REDIS_DB"),
    password=os.getenv("REDIS_PASSWORD")
)
