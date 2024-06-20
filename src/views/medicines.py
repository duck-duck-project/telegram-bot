from collections.abc import Iterable

from models import Medicine, MedicineConsumptionResult
from services.text import format_name_with_emoji, int_gaps, render_units
from views import View

__all__ = ('MedicinesListView', 'MedicineConsumedView')


class MedicineConsumedView(View):

    def __init__(self, medicine_consumption_result: MedicineConsumptionResult):
        self.__medicine_consumption_result = medicine_consumption_result

    def get_text(self) -> str:
        result = self.__medicine_consumption_result
        return (
            f'✅ Вы употребили лекарство <b>{result.medicine_name}</b>\n'
            f'❤️‍🩹 Ваше здоровье: {render_units(result.user_health)}'
            f' (+{render_units(result.health_benefit_value)})\n'
        )


class MedicinesListView(View):

    def __init__(self, medicines: Iterable[Medicine]):
        self.__medicines = tuple(medicines)

    def get_text(self) -> str:
        lines: list[str] = ['<b>Название | влияние на здоровье | цена </b>']

        for medicine in self.__medicines:
            lines.append(
                f'{format_name_with_emoji(medicine)}'
                f' | +{render_units(medicine.health_benefit_value)}'
                f' | {int_gaps(medicine.price)}'
            )

        return '\n'.join(lines)
