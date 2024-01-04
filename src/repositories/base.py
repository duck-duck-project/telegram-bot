from collections.abc import Callable
from typing import TypeAlias

import httpx
from redis.asyncio import Redis

__all__ = (
    'HTTPClientFactory',
    'APIRepository',
    'RedisRepository',
)

HTTPClientFactory: TypeAlias = Callable[..., httpx.AsyncClient]


class APIRepository:

    def __init__(self, http_client: httpx.AsyncClient):
        self._http_client = http_client


class RedisRepository:

    def __init__(self, redis: Redis):
        self._redis = redis
