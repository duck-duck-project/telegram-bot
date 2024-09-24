from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from repositories import RelationshipRepository
from views import RelationshipDetailView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text.lower() == 'мои отношения',
    StateFilter('*'),
)
async def on_show_relationship(
        message: Message,
        relationship_repository: RelationshipRepository
) -> None:
    relationship = await relationship_repository.get_by_id(message.from_user.id)
    view = RelationshipDetailView(relationship)
    await answer_view(message=message, view=view)
