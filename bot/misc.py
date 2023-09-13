import os

from aioredis import Redis

redis = Redis(host=os.getenv("REDIS_HOST"), db=0)
