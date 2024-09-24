from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import RelationshipOfferCallbackData
from repositories import RelationshipRepository
from views import RelationshipAcceptView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    RelationshipOfferCallbackData.filter(),
    StateFilter('*'),
)
async def on_accept_relationship_offer(
        callback_query: CallbackQuery,
        callback_data: RelationshipOfferCallbackData,
        relationship_repository: RelationshipRepository,
) -> None:
    if callback_data.from_user_id == callback_query.from_user.id:
        await callback_query.answer(
            text='😔 Подождите пока предложение будет принято',
            show_alert=True
        )
        return
    if callback_data.to_user_id != callback_query.from_user.id:
        await callback_query.answer(
            text='😔 Это предложение не для вас',
            show_alert=True
        )
        return
    relationship_create_result = await relationship_repository.create(
        from_user_id=callback_data.from_user_id,
        to_user_id=callback_data.to_user_id,
    )
    view = RelationshipAcceptView(relationship_create_result)
    await callback_query.answer(
        text='💚 Вы приняли предложение встречаться',
        show_alert=True
    )
    await answer_view(message=callback_query.message, view=view)
    await callback_query.message.delete_reply_markup()
