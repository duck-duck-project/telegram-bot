from collections.abc import Callable, Iterable
from typing import Never, TypeAlias, TypedDict

import httpx
from redis.asyncio import Redis

from enums import ServerApiErrorCode
from exceptions import (
    ContactAlreadyExistsError, ContactDoesNotExistError,
    SecretMessageDoesNotExistError,
    ServerAPIError,
)

__all__ = (
    'HTTPClientFactory',
    'APIRepository',
    'RedisRepository',
    'handle_server_api_errors',
)

HTTPClientFactory: TypeAlias = Callable[..., httpx.AsyncClient]


class ErrorTypedDict(TypedDict):
    code: ServerApiErrorCode
    detail: str
    attr: str | None


def handle_server_api_errors(errors: Iterable[ErrorTypedDict]) -> Never:
    error_code_to_exception_class = {
        ServerApiErrorCode.CONTACT_NOT_FOUND: ContactDoesNotExistError,
        ServerApiErrorCode.CONTACT_ALREADY_EXISTS: ContactAlreadyExistsError,
        ServerApiErrorCode.SECRET_TEXT_MESSAGE_NOT_FOUND: (
            SecretMessageDoesNotExistError
        ),
    }
    for error in errors:
        try:
            exception_class = error_code_to_exception_class[error['code']]
        except KeyError:
            raise ServerAPIError
        else:
            raise exception_class
    raise ServerAPIError


class APIRepository:

    def __init__(self, http_client: httpx.AsyncClient):
        self._http_client = http_client


class RedisRepository:

    def __init__(self, redis: Redis):
        self._redis = redis
