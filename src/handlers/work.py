from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command, StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import reply_message_from_bot_filter, integer_filter
from models import User
from repositories import BalanceRepository
from services import (
    get_arithmetic_expression,
    extract_arithmetic_problem,
    PrivateChatNotifier,
    compute_amount_to_deposit,
)
from views import (
    ArithmeticProblemView,
    ArithmeticProblemSolvedView,
    answer_view,
)

router = Router(name=__name__)


@router.message(
    F.reply_to_message.text.startswith('❓ Сколько будет'),
    F.reply_to_message.text.contains('[решено]'),
    invert_f(integer_filter),
    StateFilter('*'),
)
async def on_arithmetic_expression_answer_is_not_integer(
        message: Message
) -> None:
    await message.reply('❌ Ответ должен быть целым числом')


@router.message(
    F.reply_to_message.text.startswith('❓ Сколько будет'),
    F.reply_to_message.text.contains('[решено]'),
    StateFilter('*'),
)
async def on_arithmetic_expression_already_solved(message: Message) -> None:
    await message.reply('❌ Это задание уже решено')


@router.message(
    F.reply_to_message.text.startswith('❓ Сколько будет'),
    invert_f(F.reply_to_message.text.contains('[решено]')),
    integer_filter,
    reply_message_from_bot_filter,
    StateFilter('*'),
)
async def on_arithmetic_expression_answer(
        message: Message,
        number: int,
        user: User,
        balance_repository: BalanceRepository,
        private_chat_notifier: PrivateChatNotifier,
) -> None:
    text = f'{message.reply_to_message.text}\n\n<i>[решено]</i>'
    arithmetic_problem = extract_arithmetic_problem(
        text=message.reply_to_message.text,
    )
    if arithmetic_problem.correct_answer != number:
        await message.reply('Неправильно')
        return

    amount_to_deposit = compute_amount_to_deposit(user)

    await message.reply_to_message.edit_text(text)
    deposit = await balance_repository.create_deposit(
        user_id=message.from_user.id,
        amount=amount_to_deposit,
        description='Solved arithmetic problem',
    )
    view = ArithmeticProblemSolvedView(amount_to_deposit)
    await answer_view(message=message, view=view)
    if message.chat.type != ChatType.PRIVATE:
        await private_chat_notifier.send_deposit_notification(deposit)


@router.message(
    Command('work'),
    StateFilter('*'),
)
async def on_create_arithmetic_expression_to_solve(
        message: Message,
        state: FSMContext,
) -> None:
    await state.clear()

    expression = get_arithmetic_expression()
    view = ArithmeticProblemView(expression)
    await answer_view(message=message, view=view)
