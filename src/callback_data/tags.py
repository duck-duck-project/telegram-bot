from aiogram.filters.callback_data import CallbackData

from enums import TagWeight

__all__ = ('TagDeleteCallbackData',)


class TagDeleteCallbackData(CallbackData, prefix='tag-delete'):
    tag_id: int
    tag_weight: TagWeight
