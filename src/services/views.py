import structlog
from aiogram.exceptions import TelegramAPIError
from structlog.stdlib import BoundLogger

from views import View

__all__ = ('send_view',)

logger: BoundLogger = structlog.get_logger('app')


async def send_view(
        *,
        bot,
        chat_id: int,
        view: View,
) -> None:
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=view.get_text(),
            reply_markup=view.get_reply_markup(),
            disable_notification=view.get_disable_notification(),
        )
    except TelegramAPIError:
        await logger.aexception('Could not send view to user')
