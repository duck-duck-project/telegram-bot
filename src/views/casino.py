from views.base import View

__all__ = (
    'CasinoFAQView',
    'BetFailedView',
    'BetWonView',
)


class CasinoFAQView(View):
    text = (
        '🎲 Сделать ставку:'
        '\n\n'
        '🎨 <b>1. По цвету</b>'
        '\n'
        '<code>/bet {red или black} {сумма}</code>'
        '\n'
        'Выигрыш: 1.9x'
        '\n\n'
        '🔢 <b>2. На конкретное число</b>'
        '\n'
        '<code>/bet {число от 0 до 36} {сумма}</code>'
        '\n'
        'Выигрыш: 36х'
        '\n\n'
        '⚖️ <b>3. На четное или нечетное число</b>'
        '\n'
        '<code>/bet {even или odd} {сумма}</code>'
        '\n'
        'Выигрыш: 1.9x'
        '\n\n'
        'Сумма должна быть от 10 до 1 000 000 дак-дак коинов'
    )


class BetFailedView(View):

    def __init__(self, number: int, bet_amount: int):
        self.__number = number
        self.__bet_amount = bet_amount

    def get_text(self) -> str:
        return (
            f'Вам выпало число {self.__number},'
            f' вы проиграли {self.__bet_amount} дак-дак коинов!'
        )


class BetWonView(View):

    def __init__(self, number: int, bet_amount: int):
        self.__number = number
        self.__bet_amount = bet_amount

    def get_text(self) -> str:
        return (
            f'Вам выпало число {self.__number},'
            f' вы выиграли {self.__bet_amount} дак-дак коинов!'
        )
