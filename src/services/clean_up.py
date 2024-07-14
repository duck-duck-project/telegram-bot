from aiogram.types import Message
from redis.asyncio import Redis

__all__ = ('CleanUpService',)


class CleanUpService:

    def __init__(self, redis: Redis):
        self.__redis = redis

    async def create_clean_up_task(
            self,
            *messages: Message,
    ):
        values = [
            f'{message.chat.id}:{message.message_id}'
            for message in messages
        ]
        await self.__redis.rpush('duck-duck:clean-up', *values)
