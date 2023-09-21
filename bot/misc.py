import os

from redis.asyncio import Redis

redis = Redis(
    host=os.getenv("REDIS_HOST"),
    db=0,
    password=os.getenv("REDIS_PASSWORD")
)
