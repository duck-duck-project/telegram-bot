from collections.abc import Iterable
from datetime import timedelta

import humanize

from models import SportActivity
from services.food import render_energy
from views import View

__all__ = (
    'SportActivitiesThrottledView',
    'NotEnoughHealthView',
    'SportActivityDoneView',
    'SportActivitiesListView',
)


class NotEnoughHealthView(View):

    def __init__(self, health_cost_value: int):
        self.__health_cost_value = health_cost_value

    def get_text(self) -> str:
        return (
            '❌ Недостаточно здоровья\n'
            '❤️‍🩹 Требуется'
            f' {render_energy(self.__health_cost_value)} здоровья\n\n'
            'Чтобы восполнить здоровье вы можете:\n'
            '- Правильно питаться\n'
            '- Заняться спортом (команда <code>заняться спортом</code>)\n'
            '- Принять лекарства (в разработке)'
        )


class SportActivitiesThrottledView(View):

    def __init__(self, next_sports_in_seconds: int):
        self.__next_sports_in_seconds = next_sports_in_seconds

    def get_text(self) -> str:
        next_activity = humanize.precisedelta(
            timedelta(seconds=self.__next_sports_in_seconds),
        )
        return f'❌ Следующее занятие спортом через: {next_activity}'


class SportActivityDoneView(View):

    def __init__(self, sport_activity: SportActivity, current_health: int):
        self.__sport_activity = sport_activity
        self.__current_health = current_health

    def get_text(self) -> str:
        sport_activity_name = self.__sport_activity.name
        health_benefit_value = self.__sport_activity.health_benefit_value
        return (
            f'✅ Вы выполнили упражнение <b>{sport_activity_name}</b>\n'
            '❤️‍🩹 Восстановлено'
            f' {render_energy(health_benefit_value)} здоровья\n'
            '🏥 Текущее здоровье:'
            f' {render_energy(self.__current_health)} из 100\n'
        )


class SportActivitiesListView(View):

    def __init__(self, sport_activities: Iterable[SportActivity]):
        self.__sport_activities = tuple(sport_activities)

    def get_text(self) -> str:
        lines: list[str] = [
            '<b>Название | нужно энергии | прибавка здоровья</b>',
        ]

        for sport_activity in self.__sport_activities:
            lines.append(
                f'{sport_activity.name}'
                f' | {render_energy(sport_activity.energy_cost_value)}'
                f' | {render_energy(sport_activity.health_benefit_value)}',
            )

        lines.append(
            '\n❓ Используйте команду'
            ' <code>заняться спортом {название}</code>'
            ' чтобы восстановить здоровье'
        )

        return '\n'.join(lines)
