from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from views.base import View

__all__ = ('ObisLoginView',)


class ObisLoginView(View):
    text = (
        '👇 Нажмите кнопку ниже чтобы войти в OBIS.'
        '\n<b>❗️ Никому не пересылайте кнопку ниже.'
        ' Иначе они смогут получить доступ к вашему аккаунту</b>'
    )

    def __init__(self, login_url: str):
        self.__login_url = login_url

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='🚀 Перейти в OBIS',
                        url=self.__login_url,
                    )
                ],
            ],
        )
