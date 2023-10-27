from collections.abc import Callable, Awaitable
from typing import TypeAlias, Protocol, Coroutine, Any

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message

from exceptions import UnsupportedContentTypeError
from models import SecretMediaType
from views import AnonymousMessageSentView, answer_view

__all__ = (
    'extract_file_id_from_message',
    'AnonymousMessageSender',
    'is_anonymous_messaging_enabled',
    'determine_media_file',
    'get_message_method_by_media_type',
)

ReturnsMessage: TypeAlias = Callable[..., Awaitable[Message]]


class HasFileID(Protocol):
    file_id: str


def is_anonymous_messaging_enabled(state_name: str) -> bool:
    # rename it if state declaration will be changed
    # in anonymous_messaging.states.py file
    return state_name == 'AnonymousMessagingStates:enabled'


def determine_media_file(message: Message) -> tuple[str, SecretMediaType]:
    medias_and_media_types: list[tuple[HasFileID, SecretMediaType]] = [
        (message.voice, SecretMediaType.VOICE),
        (message.video, SecretMediaType.VIDEO),
        (message.audio, SecretMediaType.AUDIO),
        (message.animation, SecretMediaType.ANIMATION),
        (message.document, SecretMediaType.DOCUMENT),
        (message.video_note, SecretMediaType.VIDEO_NOTE),
        (message.sticker, SecretMediaType.STICKER),
    ]
    if message.photo:
        medias_and_media_types.append(
            (message.photo[-1], SecretMediaType.PHOTO)
        )
    for media, media_type in medias_and_media_types:
        if media is not None:
            return media.file_id, media_type
    raise ValueError('Unsupported media type')


def extract_file_id_from_message(message: Message) -> str:
    medias = (
        message.photo,
        message.voice,
        message.animation,
        message.video,
        message.video_note,
        message.sticker,
        message.document,
        message.audio,
    )
    for media in medias:
        if media is not None:
            if isinstance(media, list):
                return media[-1].file_id
            return media.file_id

    raise UnsupportedContentTypeError(content_type=message.content_type)


def get_message_method_by_media_type(
        *,
        message: Message,
        media_type: SecretMediaType,
) -> Callable[..., Coroutine[Any, Any, Message]]:
    media_type_to_method = {
        SecretMediaType.PHOTO: message.answer_photo,
        SecretMediaType.VOICE: message.answer_voice,
        SecretMediaType.ANIMATION: message.answer_animation,
        SecretMediaType.VIDEO: message.answer_video,
        SecretMediaType.VIDEO_NOTE: message.answer_video_note,
        SecretMediaType.STICKER: message.answer_sticker,
        SecretMediaType.DOCUMENT: message.answer_document,
        SecretMediaType.AUDIO: message.answer_audio,
    }
    try:
        return media_type_to_method[media_type]
    except KeyError:
        raise ValueError('Unsupported media type')


class AnonymousMessageSender:

    def __init__(self, bot: Bot):
        self.__bot = bot

    async def send_text(self, *, chat_id: int | str, message: Message) -> None:
        try:
            text = f'<b>💌 Анонимное сообщение</b>\n\n{message.text}'
            await self.__bot.send_message(chat_id, text)
        except TelegramAPIError as error:
            await self.__bot.send_message(
                chat_id=chat_id,
                text=f'❌ Не получилось отправить. Ошибка: {str(error)}',
            )
        else:
            await answer_view(message=message, view=AnonymousMessageSentView())

    async def send_media(self, chat_id: int, message: Message) -> None:
        text = '<b>💌 Анонимное сообщение</b>'
        if message.caption is not None:
            text += f'\n\n{message.caption}'

        content_type = message.content_type
        content_type_to_method: dict[str | ContentType, ReturnsMessage] = {
            ContentType.PHOTO: self.__bot.send_photo,
            ContentType.VIDEO: self.__bot.send_video,
            ContentType.ANIMATION: self.__bot.send_animation,
            ContentType.VOICE: self.__bot.send_voice,
            ContentType.AUDIO: self.__bot.send_audio,
            ContentType.DOCUMENT: self.__bot.send_document,
            ContentType.VIDEO_NOTE: self.__bot.send_video_note,
            ContentType.STICKER: self.__bot.send_sticker,
        }

        try:
            method = content_type_to_method[content_type]
        except KeyError:
            raise UnsupportedContentTypeError(content_type=content_type)

        file_id = extract_file_id_from_message(message)

        # Due to Telegram API limitations, we can't send sticker or video note
        # with caption, so we send media without caption
        # and then send caption as a separate message.
        try:
            if content_type in {ContentType.STICKER, ContentType.VIDEO_NOTE}:
                sent_media = await method(chat_id, file_id)
                await sent_media.reply(text)
            else:
                await method(chat_id, file_id, caption=text)
        except TelegramAPIError as error:
            await self.__bot.send_message(
                chat_id=chat_id,
                text=f'❌ Не получилось отправить. Ошибка: {str(error)}',
            )
        else:
            await answer_view(message=message, view=AnonymousMessageSentView())
