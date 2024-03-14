from uuid import uuid4

from aiogram import F, Router
from aiogram.filters import StateFilter, invert_f
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineQuery, InlineQueryResultArticle

from filters import secret_message_text_length_filter
from models import User
from repositories import ContactRepository
from services import filter_not_hidden
from views import (
    NoUserContactsInlineQueryView,
    NoVisibleContactsInlineQueryView,
    SecretMessageDetailInlineQueryView,
    SecretMessageTextMissingInlineQueryView,
    TooLongSecretMessageTextInlineQueryView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.inline_query(
    invert_f(F.query),
    StateFilter('*'),
)
async def on_secret_message_text_missing(inline_query: InlineQuery) -> None:
    items = [
        SecretMessageTextMissingInlineQueryView()
        .get_inline_query_result_article()
    ]
    await inline_query.answer(items, cache_time=1)


@router.inline_query(
    invert_f(secret_message_text_length_filter),
    StateFilter('*'),
)
async def on_secret_message_text_too_long(
        inline_query: InlineQuery,
) -> None:
    items = [
        TooLongSecretMessageTextInlineQueryView()
        .get_inline_query_result_article()
    ]
    await inline_query.answer(items, cache_time=1, is_personal=True)


@router.inline_query(
    secret_message_text_length_filter,
    StateFilter('*'),
)
async def on_secret_message_typing(
        inline_query: InlineQuery,
        contact_repository: ContactRepository,
        state: FSMContext,
        text: str,
        user: User,
) -> None:
    contacts = await contact_repository.get_by_user_id(user.id)

    if not contacts:
        items = [
            NoUserContactsInlineQueryView().get_inline_query_result_article()
        ]
        await inline_query.answer(items, cache_time=1, is_personal=True)
        return

    visible_contacts = filter_not_hidden(contacts)

    if not visible_contacts:
        items = [
            NoVisibleContactsInlineQueryView().get_inline_query_result_article()
        ]
        await inline_query.answer(items, cache_time=1, is_personal=True)
        return

    draft_secret_message_id = uuid4()
    await state.update_data(secret_message_id=draft_secret_message_id.hex)

    contacts_and_query_ids = [
        (contact, f'{uuid4().hex}@{contact.to_user.id}')
        for contact in visible_contacts
    ]

    items: list[InlineQueryResultArticle] = [
        SecretMessageDetailInlineQueryView(
            query_id=query_id,
            contact=contact,
            secret_message_id=draft_secret_message_id,
            theme=user.theme,
        ).get_inline_query_result_article()
        for contact, query_id in contacts_and_query_ids
    ]
    await inline_query.answer(items, cache_time=1, is_personal=True)
