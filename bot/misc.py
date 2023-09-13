import os

from aioredis import Redis

redis = Redis(
        host=os.getenv('REDIS_HOST') or '127.0.0.1',
        password=os.getenv('REDIS_PASSWORD') or None,
        username=os.getenv('REDIS_USER') or None,
)
