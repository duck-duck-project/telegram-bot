import aiohttp
import structlog
from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from structlog.stdlib import BoundLogger

from exceptions import ServerAPIError
from views import (
    ClientConnectorErrorInlineQueryView,
    ServerAPIErrorInlineQueryView,
)

__all__ = ('router',)

logger: BoundLogger = structlog.get_logger('app')

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(aiohttp.ClientConnectorError))
async def on_client_connector_error(event: ErrorEvent) -> None:
    update = event.update
    text = '❌ Ошибка подключения к серверу, попробуйте позже'
    if update.message is not None:
        await update.message.answer(text)
    if update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    if update.inline_query is not None:
        await update.inline_query.answer([
            ClientConnectorErrorInlineQueryView()
            .get_inline_query_result_article()
        ], is_personal=True)
    await logger.acritical('Can not connect to the API server')


@router.error(ExceptionTypeFilter(ServerAPIError))
async def on_server_api_error(event: ErrorEvent) -> None:
    update = event.update
    text = '❌ Ошибка API сервера, попробуйте позже'
    if update.message is not None:
        await update.message.answer(text)
    if update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    if update.inline_query is not None:
        await update.inline_query.answer([
            ServerAPIErrorInlineQueryView()
            .get_inline_query_result_article()
        ])
    await logger.acritical('Error on the API server side')
