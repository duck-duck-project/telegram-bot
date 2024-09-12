from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from exceptions import MedicineDoesNotExistError
from filters import medicine_filter
from repositories import MedicineRepository
from views import MedicineConsumedView, MedicinesListView, reply_view

router = Router(name=__name__)


@router.message(
    medicine_filter,
    StateFilter('*'),
)
async def on_consume_medicine(
        message: Message,
        medicine_repository: MedicineRepository,
        medicine_name: str,
) -> None:
    try:
        medicine_consumption_result = await medicine_repository.consume(
            user_id=message.from_user.id,
            medicine_name=medicine_name,
        )
    except MedicineDoesNotExistError:
        await message.reply('Такого лекарства нет в моем ассортименте')
    else:
        view = MedicineConsumedView(medicine_consumption_result)
        await reply_view(message=message, view=view)


@router.message(
    F.text.lower().startswith('лекарство'),
    StateFilter('*'),
)
async def on_show_medicines_list(
        message: Message,
        medicine_repository: MedicineRepository,
) -> None:
    medicines = await medicine_repository.get_all()
    view = MedicinesListView(medicines)
    await reply_view(message=message, view=view)
