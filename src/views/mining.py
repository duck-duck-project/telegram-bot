from datetime import timedelta

import humanize

from models import MinedResource, MiningUserStatistics
from views import View

__all__ = (
    'MinedResourceView',
    'MiningActionThrottledView',
    'MiningStatisticsView',
)


class MiningActionThrottledView(View):

    def __init__(self, next_mining_in_seconds: int):
        self.__next_mining_in_seconds = next_mining_in_seconds

    def get_text(self) -> str:
        next_mining = humanize.precisedelta(
            timedelta(seconds=self.__next_mining_in_seconds),
        )
        return f'❌ Следующая добыча через: {next_mining}'


class MinedResourceView(View):

    def __init__(self, mined_resource: MinedResource):
        self.__mined_resource = mined_resource

    def get_text(self) -> str:
        return (
            f'⛏️ Вы добыли ресурс "{self.__mined_resource.resource_name}"'
            f' на сумму {self.__mined_resource.wealth} дак-дак коинов!'
        )


class MiningStatisticsView(View):

    def __init__(self, mining_statistics: MiningUserStatistics):
        self.__mining_statistics = mining_statistics

    def get_text(self) -> str:
        if not self.__mining_statistics.resources:
            return (
                '😔 Вы ещё не работали на шахте.\n'
                'Чтобы начать, введите <code>шахта</code>'
                ' или <code>копать</code>'
            )

        emojis = ('▪️', '▫️')
        lines: list[str] = ['<b>⛏️ Статистика шахты:</b>']
        for index, resource in enumerate(self.__mining_statistics.resources):
            emoji = emojis[index % 2]
            lines.append(
                f'{emoji} {resource.name} - {resource.total_count} раз - {resource.total_wealth} дак-дак коинов'
            )
        return '\n'.join(lines)
