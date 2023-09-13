from aiogram.fsm.storage.redis import RedisStorage

redis = RedisStorage.from_url('redis://localhost:6379/0')
