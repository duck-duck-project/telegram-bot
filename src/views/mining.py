from collections.abc import Iterable
from datetime import timedelta

import humanize

from models import (
    MinedResourceResult, MinedResourceStatistics, MiningChatStatistics,
    MiningUserStatistics,
)
from services.text import render_grams, render_units
from views import PhotoView, View

__all__ = (
    'MinedResourceView',
    'MinedResourcePhotoView',
    'MiningActionThrottledView',
    'MiningUserStatisticsView',
    'MiningChatStatisticsView',
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
        energy = self.__mined_resource_result.remaining_energy
        emoji = '🪫' if energy < 5000 else '🔋'
        my_energy = f'{emoji} Ваша энергия: {render_units(energy)} из 100'
        spent_energy = render_units(self.__mined_resource_result.spent_energy)
        return (
            f'⛏️ Вы добыли {weight} ресурса "{resource_name}"'
            f' на сумму {value} дак-дак коинов!\n'
            f'⚡️ Потрачено {spent_energy} энергии\n'
            f'{my_energy}'
        )


class MinedResourcePhotoView(PhotoView, MinedResourceView):

    def __init__(
            self,
            mined_resource_result: MinedResourceResult,
            photo_url: str,
    ):
        super().__init__(mined_resource_result)
        self.__photo_url = photo_url

    def get_caption(self) -> str:
        return self.get_text()

    def get_photo(self) -> str:
        return self.__photo_url


def compute_total_value(
        mined_resources: Iterable[MinedResourceStatistics],
) -> int:
    return sum(resource.total_value for resource in mined_resources)


def compute_total_count(
        mined_resources: Iterable[MinedResourceStatistics],
) -> int:
    return sum(resource.total_count for resource in mined_resources)


def render_total_statistics(
        mined_resources: Iterable[MinedResourceStatistics],
) -> str:
    total_value = compute_total_value(mined_resources)
    total_count = compute_total_count(mined_resources)
    return f'<b>Всего: {total_count} раз - {total_value} коинов</b>'


def render_resources_list(
        mined_resources: Iterable[MinedResourceStatistics],
) -> list[str]:
    emojis = ('▪️', '▫️')
    lines: list[str] = []
    for index, resource in enumerate(mined_resources):
        emoji = emojis[index % 2]
        lines.append(
            f'{emoji} {resource.name} - {resource.total_count} раз'
            f' - {resource.total_value} коинов'
        )
    return lines


class MiningUserStatisticsView(View):

    def __init__(self, mining_statistics: MiningUserStatistics):
        self.__mining_statistics = mining_statistics

    def get_text(self) -> str:
        if not self.__mining_statistics.resources:
            return (
                '😔 Вы ещё не работали на шахте.\n'
                'Чтобы начать, введите <code>шахта</code>'
                ' или <code>копать</code>'
            )
        lines: list[str] = ['<b>⛏️ Статистика шахты:</b>']

        lines += render_resources_list(self.__mining_statistics.resources)

        if len(self.__mining_statistics.resources) > 1:
            lines.append(
                render_total_statistics(self.__mining_statistics.resources)
            )
        return '\n'.join(lines)


class MiningChatStatisticsView(View):

    def __init__(self, mining_statistics: MiningChatStatistics):
        self.__mining_statistics = mining_statistics

    def get_text(self) -> str:
        if not self.__mining_statistics.resources:
            return '😔 На шахте ещё никто не работал.'

        lines: list[str] = ['<b>⛏️ Статистика шахты этого чата:</b>']

        lines += render_resources_list(self.__mining_statistics.resources)

        if len(self.__mining_statistics.resources) > 1:
            lines.append(
                render_total_statistics(self.__mining_statistics.resources)
            )
        lines.append(
            f'<b>Глубина шахты чата: '
            f'{len(self.__mining_statistics.resources)}</b>'
        )
        return '\n'.join(lines)
