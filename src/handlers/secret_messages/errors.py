from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from exceptions import SecretMessageDoesNotExistError
from repositories import HTTPClientFactory, UserRepository

__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(SecretMessageDoesNotExistError))
async def on_secret_message_does_not_exist_error(
        event: ErrorEvent,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    user_id = event.update.callback_query.from_user.id
    async with closing_http_client_factory() as http_client:
        user_repository = UserRepository(http_client)
        user = await user_repository.get_by_id(user_id)
    if user.theme is None:
        text = (
            'Сообщение не найдено.'
            ' Возможно оно ещё не загружено на наши сервера.'
            ' Попробуйте через пару секунд',
        )
    else:
        text = user.theme.secret_message_missing_text
    await event.update.callback_query.answer(text, show_alert=True)
