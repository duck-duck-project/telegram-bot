from datetime import timedelta

import humanize

from models import MinedResourceResult, MiningUserStatistics
from services.text import render_grams
from services.food import render_energy, render_my_energy
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

    def __init__(self, mined_resource_result: MinedResourceResult):
        self.__mined_resource_result = mined_resource_result

    def get_text(self) -> str:
        weight = render_grams(self.__mined_resource_result.weight_in_grams)
        resource_name = self.__mined_resource_result.resource_name
        value = self.__mined_resource_result.value
        spent_energy = render_energy(self.__mined_resource_result.spent_energy)
        my_energy = render_my_energy(
            energy=self.__mined_resource_result.remaining_energy,
        )
        return (
            f'⛏️ Вы добыли {weight} ресурса "{resource_name}"'
            f' на сумму {value} дак-дак коинов!\n'
            f'⚡️ Потрачено {spent_energy} энергии\n'
            f'{my_energy}'
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
                f'{emoji} {resource.name} - {resource.total_count} раз'
                f' - {resource.total_value} коинов'
            )

        if len(self.__mining_statistics.resources) > 1:
            total_wealth = sum(
                resource.total_value
                for resource in self.__mining_statistics.resources
            )
            total_count = sum(
                resource.total_count
                for resource in self.__mining_statistics.resources
            )
            lines.append(
                f'<b>Всего: {total_count} раз - {total_wealth} коинов</b>'
            )
        return '\n'.join(lines)
