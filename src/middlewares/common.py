from collections.abc import Callable, MutableMapping, Awaitable
from typing import TypeAlias, Any

from aiogram.types import Update, Message, CallbackQuery, InlineQuery

__all__ = ('ContextData', 'Handler', 'HandlerReturn')

Event: TypeAlias = Update | Message | CallbackQuery | InlineQuery
ContextData: TypeAlias = MutableMapping[str, Any]
Handler: TypeAlias = Callable[[Event, ContextData], Awaitable[Any]]
HandlerReturn: TypeAlias = Any
