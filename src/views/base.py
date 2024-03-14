from typing import TypeAlias, assert_never
from uuid import uuid4

from aiogram import Bot
from aiogram.types import (
    CallbackQuery, ForceReply, InlineKeyboardMarkup, InlineQueryResultArticle,
    InputFile, InputTextMessageContent, Message, ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

__all__ = (
    'ReplyMarkup',
    'View',
    'answer_view',
    'edit_message_by_view',
    'InlineQueryView',
    'render_message_or_callback_query',
    'send_view',
    'reply_view',
    'PhotoView',
    'answer_photo_view',
    'MediaGroupView',
    'answer_media_group_view',
    'CallbackQueryAnswerView',
    'answer_callback_query',
)

from aiogram.utils.media_group import MediaType, MediaGroupBuilder

ReplyMarkup: TypeAlias = (
        InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ForceReply
        | ReplyKeyboardRemove
)


class View:
    text: str | None = None
    reply_markup: ReplyMarkup | None = None
    disable_notification: bool | None = None
    disable_web_page_preview: bool | None = None

    def get_text(self) -> str | None:
        return self.text

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup

    def get_disable_notification(self) -> bool | None:
        return self.disable_notification

    def get_disable_web_page_preview(self) -> bool | None:
        return self.disable_web_page_preview


class PhotoView:
    photo: str | InputFile
    caption: str | None = None
    reply_markup: ReplyMarkup | None = None

    def get_photo(self) -> str | InputFile:
        return self.photo

    def get_caption(self) -> str | None:
        return self.caption

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup


class MediaGroupView:
    medias: list[MediaType] | None = None
    caption: str | None = None

    def get_caption(self) -> str | None:
        return self.caption

    def get_medias(self) -> list[MediaType] | None:
        return self.medias

    def as_media_group(self) -> list[MediaType]:
        media_group_builder = MediaGroupBuilder(
            media=self.get_medias(),
            caption=self.get_caption(),
        )
        return media_group_builder.build()


class CallbackQueryAnswerView:
    text: str
    show_alert: bool = False

    def get_text(self) -> str:
        return self.text

    def get_show_alert(self) -> bool:
        return self.show_alert


class InlineQueryView(View):
    title: str
    description: str | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None

    def get_id(self) -> str:
        return uuid4().hex

    def get_title(self) -> str:
        return self.title

    def get_description(self) -> str | None:
        return self.description

    def get_thumbnail_url(self) -> str | None:
        return self.thumbnail_url

    def get_thumbnail_width(self) -> int | None:
        return self.thumbnail_width

    def get_thumbnail_height(self) -> int | None:
        return self.thumbnail_height

    def get_inline_query_result_article(self) -> InlineQueryResultArticle:
        return InlineQueryResultArticle(
            id=self.get_id(),
            title=self.get_title(),
            description=self.get_description(),
            input_message_content=InputTextMessageContent(
                message_text=self.get_text(),
            ),
            reply_markup=self.get_reply_markup(),
            thumb_url=self.get_thumbnail_url(),
            thumb_width=self.get_thumbnail_width(),
            thumb_height=self.get_thumbnail_height(),
        )


async def answer_media_group_view(
        *,
        message: Message,
        view: MediaGroupView,
) -> list[Message]:
    return await message.answer_media_group(
        media=view.as_media_group(),
    )


async def answer_view(
        *,
        message: Message,
        view: View,
) -> Message:
    return await message.answer(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
        disable_web_page_preview=view.get_disable_web_page_preview(),
        disable_notification=view.get_disable_notification(),
    )


async def answer_photo_view(
        *,
        message: Message,
        view: PhotoView,
) -> Message:
    return await message.answer_photo(
        photo=view.get_photo(),
        caption=view.get_caption(),
        reply_markup=view.get_reply_markup(),
    )


async def reply_view(
        *,
        message: Message,
        view: View,
) -> Message:
    return await message.reply(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
        disable_notification=view.get_disable_notification(),
        disable_web_page_preview=view.get_disable_web_page_preview(),
    )


async def edit_message_by_view(
        *,
        message: Message,
        view: View,
) -> Message:
    return await message.edit_text(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
        disable_web_page_preview=view.get_disable_web_page_preview(),
    )


async def render_message_or_callback_query(
        *,
        message_or_callback_query: Message | CallbackQuery,
        view: View,
) -> Message:
    match message_or_callback_query:
        case Message():
            return await answer_view(
                message=message_or_callback_query,
                view=view,
            )
        case CallbackQuery():
            return await edit_message_by_view(
                message=message_or_callback_query.message,
                view=view,
            )
        case _:
            assert_never(message_or_callback_query)


async def send_view(
        *,
        bot: Bot,
        chat_id: int,
        view: View,
) -> Message:
    return await bot.send_message(
        chat_id=chat_id,
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
        disable_notification=view.get_disable_notification(),
        disable_web_page_preview=view.get_disable_web_page_preview(),
    )


async def answer_callback_query(
        *,
        callback_query: CallbackQuery,
        view: CallbackQueryAnswerView,
) -> bool:
    return await callback_query.answer(
        text=view.get_text(),
        show_alert=view.get_show_alert(),
    )
