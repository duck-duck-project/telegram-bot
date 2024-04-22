from aiogram.filters.callback_data import CallbackData

from enums import TagWeight

__all__ = ('TagDeleteCallbackData', 'TagListCallbackData')


class TagDeleteCallbackData(CallbackData, prefix='tag-delete'):
    tag_id: int
    tag_weight: TagWeight


class TagListCallbackData(CallbackData, prefix='tag-list'):
    user_id: int
    user_full_name: str
