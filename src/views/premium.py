import textwrap

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from views.base import View

__all__ = (
    'PremiumSubscriptionLinkView',
    'PremiumSubscriptionInfoView',
)


class PremiumSubscriptionLinkView(View):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='❓ Что это мне даёт',
                    callback_data='show-premium-subscription',
                ),
            ],
            [
                InlineKeyboardButton(
                    text='🚀 Купить подписку',
                    url='https://t.me/usbtypec',
                ),
            ],
        ],
    )

    def __init__(self, text):
        self.__text = text

    def get_text(self) -> str:
        return self.__text


class PremiumSubscriptionInfoView(View):
    text = textwrap.dedent('''
        ✨ <b>Преимущества премиум-подписки:</b>
        - 📊 Увеличенный лимит на количество символов в секретных сообщениях (200 вместо 60)
                        
        - 💸 x2 дак-дак коинов за каждую выполненную работу
        
        🔥 <b>Стоимость всего этого чуда всего 50 сомов в месяц!</b> 💰
    ''')
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='🚀 Купить подписку',
                    url='https://t.me/usbtypec',
                ),
            ],
        ],
    )
