import os

from redis.asyncio import Redis

redis = Redis(
    db=0,
    password=os.getenv("REDIS_PASSWORD")
)
