from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import (
    StateFilter,
    Command,
    invert_f,
    ExceptionTypeFilter,
    or_f,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ErrorEvent, CallbackQuery

from exceptions import InsufficientFundsForTransferError
from filters import transfer_operation_filter
from repositories import BalanceRepository, ContactRepository
from services import BalanceNotifier
from states import TransferStates
from views import (
    ContactListChooseView,
    answer_view,
    TransferAskForDescriptionView,
    TransferConfirmView, edit_message_by_view, TransferSuccessfullyExecutedView,
)

router = Router(name=__name__)


@router.message(
    or_f(
        Command('send'),
        F.text == '💳 Перевод средств',
    ),
    F.chat.type == ChatType.PRIVATE,
    StateFilter('*'),
)
async def on_start_transfer_in_private_chat(
        message: Message,
        state: FSMContext,
        contact_repository: ContactRepository,
) -> None:
    contacts = await contact_repository.get_by_user_id(message.from_user.id)
    if not contacts:
        await message.reply(
            '❌ У вас нет контактов\n'
            '👥 Добавьте контакт /contact'
        )
        return
    await state.set_state(TransferStates.contact)
    view = ContactListChooseView(contacts)
    await answer_view(message=message, view=view)


@router.error(ExceptionTypeFilter(InsufficientFundsForTransferError))
async def on_insufficient_funds_for_transfer_error(event: ErrorEvent) -> None:
    await event.update.message.reply(
        '❌ Недостаточно средств для перевода\n'
        '💸 Начните работать прямо сейчас /work'
    )


@router.message(
    Command('send'),
    invert_f(transfer_operation_filter),
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    StateFilter('*'),
)
async def on_transfer_operation_amount_invalid(
        message: Message,
) -> None:
    await message.reply(
        '💳 Отправить перевод:\n'
        '<code>/send {сумма перевода} {описание (необязательно)}</code>'
    )


@router.message(
    Command('send'),
    F.from_user.id == F.reply_to_message.from_user.id,
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    StateFilter('*'),
)
async def on_transfer_to_himself(message: Message) -> None:
    await message.reply('🤨 Нельзя переводить самому себе')


@router.message(
    F.reply_to_message,
    or_f(
        Command('send'),
        F.text.lower().startswith('pay '),
        F.text.lower().startswith('отправить '),
        F.text.lower().startswith('send '),
    ),
    invert_f(F.reply_to_message.from_user.is_bot),
    F.from_user.id != F.reply_to_message.from_user.id,
    transfer_operation_filter,
    StateFilter('*'),
)
async def on_create_transfer_in_group_chat(
        message: Message,
        amount: int,
        description: str | None,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    sender_id = message.from_user.id
    recipient_id = message.reply_to_message.from_user.id

    description = description or f'Transfer from {message.from_user.full_name}'

    transfer = await balance_repository.create_transfer(
        sender_id=sender_id,
        recipient_id=recipient_id,
        amount=amount,
        description=description,
    )
    await message.reply(
        text=f'✅ Перевод на сумму в {amount} дак-дак коинов успешно выполнен',
    )
    await balance_notifier.send_transfer_notification(transfer)


@router.callback_query(
    F.message.chat.type == ChatType.PRIVATE,
    F.data == 'cancel',
    StateFilter(TransferStates.confirm),
)
async def on_transfer_cancel(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.clear()
    await callback_query.message.edit_text('❌ Перевод отменён')


@router.callback_query(
    F.message.chat.type == ChatType.PRIVATE,
    F.data == 'confirm',
    StateFilter(TransferStates.confirm),
)
async def on_transfer_confirm(
        callback_query: CallbackQuery,
        state: FSMContext,
        balance_repository: BalanceRepository,
        balance_notifier: BalanceNotifier,
) -> None:
    state_data = await state.get_data()
    await state.clear()
    amount: int = state_data['amount']
    description: str | None = state_data['description']
    recipient_user_id: int = state_data['recipient_id']
    sender_id = callback_query.from_user.id

    transfer = await balance_repository.create_transfer(
        sender_id=sender_id,
        recipient_id=recipient_user_id,
        amount=amount,
        description=description,
    )
    await balance_notifier.send_transfer_notification(transfer)
    view = TransferSuccessfullyExecutedView(transfer)
    await edit_message_by_view(message=callback_query.message, view=view)


@router.callback_query(
    F.message.chat.type == ChatType.PRIVATE,
    F.data == 'skip',
    StateFilter(TransferStates.description),
)
async def on_description_skip(
        callback_query: CallbackQuery,
        state: FSMContext,
        contact_repository: ContactRepository,
) -> None:
    await state.set_state(TransferStates.confirm)
    state_data = await state.get_data()
    contact_id: int = state_data['contact_id']
    amount: int = state_data['amount']
    description = None
    contact = await contact_repository.get_by_id(contact_id)
    await state.update_data(
        description=description,
        recipient_id=contact.to_user.id,
    )
    view = TransferConfirmView(
        amount=amount,
        recipient_name=contact.private_name,
        description=description,
    )
    await edit_message_by_view(message=callback_query.message, view=view)


@router.message(
    F.chat.type == ChatType.PRIVATE,
    F.text,
    StateFilter(TransferStates.description),
)
async def on_enter_transfer_description(
        message: Message,
        state: FSMContext,
        contact_repository: ContactRepository,
) -> None:
    await state.set_state(TransferStates.confirm)
    state_data = await state.get_data()
    contact_id: int = state_data['contact_id']
    amount: int = state_data['amount']
    description = message.text
    contact = await contact_repository.get_by_id(contact_id)
    await state.update_data(
        description=description,
        recipient_id=contact.to_user.id,
    )
    view = TransferConfirmView(
        amount=amount,
        recipient_name=contact.private_name,
        description=description,
    )
    await answer_view(message=message, view=view)


@router.message(
    F.chat.type == ChatType.PRIVATE,
    StateFilter(TransferStates.amount),
)
async def on_enter_transfer_amount(
        message: Message,
        state: FSMContext,
        balance_repository: BalanceRepository,
) -> None:
    if not message.text.isdigit():
        await message.reply('❌ Сумма перевода должна быть целым числом')
        return

    user_id = message.from_user.id
    amount_to_transfer = int(message.text)

    user_balance = await balance_repository.get_user_balance(user_id)

    if user_balance.balance < amount_to_transfer:
        raise InsufficientFundsForTransferError

    await state.update_data(amount=amount_to_transfer)
    await state.set_state(TransferStates.description)
    view = TransferAskForDescriptionView()
    await answer_view(message=message, view=view)


@router.callback_query(
    F.message.chat.type == ChatType.PRIVATE,
    StateFilter(TransferStates.contact),
)
async def on_choose_contact_for_transfer(
        callback_query: CallbackQuery,
        state: FSMContext,
) -> None:
    await state.update_data(contact_id=int(callback_query.data))
    await state.set_state(TransferStates.amount)
    await callback_query.message.edit_text('💰 Введите сумму перевода:')
