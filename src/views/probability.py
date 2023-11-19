from views.base import View

__all__ = ('ProbabilityAnswerView',)


class ProbabilityAnswerView(View):

    def __init__(
            self,
            *,
            question: str,
            answer_emoji: str,
            probability_percent: int,
    ):
        self.__question = question
        self.__answer_emoji = answer_emoji
        self.__probability_percent = probability_percent

    def get_text(self) -> str:
        return (
            f'<i>❓ {self.__question}</i>\n'
            f'{self.__answer_emoji} <b>{self.__probability_percent}%</b>'
        )
