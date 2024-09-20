from aiogram.filters.callback_data import CallbackData

__all__ = ('RelationshipOfferCallbackData',)


class RelationshipOfferCallbackData(CallbackData, prefix='relationships-offer'):
    from_user_id: int
    to_user_id: int
