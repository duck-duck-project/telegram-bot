from collections.abc import Iterable
from datetime import timedelta

import humanize

from models import SportActivity, SportActivityActionResult
from services.text import format_name_with_emoji, render_units
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
            f' {render_units(self.__health_cost_value)} здоровья\n\n'
            'Чтобы восполнить здоровье вы можете:\n'
            '- Правильно питаться\n'
            '- Заняться спортом (команда <code>заняться спортом</code>)\n'
            '- Принять лекарства (команда <code>лекарство</code>)'
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

    def __init__(self, sport_activity_action_result: SportActivityActionResult):
        self.__sport_activity_action_result = sport_activity_action_result

    def get_text(self) -> str:
        result = self.__sport_activity_action_result
        cooldown = humanize.precisedelta(
            timedelta(seconds=result.cooldown_in_seconds)
        )
        return (
            f'✅ Вы выполнили упражнение <b>{result.sport_activity_name}</b>\n'
            f'❤️‍🩹 Ваше здоровье: {render_units(result.user_health)}'
            f' (+{render_units(result.health_benefit_value)})\n'
            f'⚡️ Ваша энергия: {render_units(result.user_energy)}'
            f' (-{render_units(result.energy_cost_value)})\n'
            f'⏱️ Следующее упражнение через: {cooldown}'
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
                f'{format_name_with_emoji(sport_activity)}'
                f' | {render_units(sport_activity.energy_cost_value)}'
                f' | +{render_units(sport_activity.health_benefit_value)}',
            )

        lines.append(
            '\n❓ Используйте команду'
            ' <code>заняться спортом {название}</code>'
            ' чтобы восстановить здоровье'
        )

        return '\n'.join(lines)
