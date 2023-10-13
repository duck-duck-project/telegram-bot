from aiogram.filters.callback_data import CallbackData

__all__ = (
    'TeamDetailCallbackData',
    'TeamUpdateCallbackData',
    'TeamDeleteAskForConfirmationCallbackData',
)


class TeamDetailCallbackData(CallbackData, prefix='team-detail'):
    team_id: int


class TeamUpdateCallbackData(CallbackData, prefix='team-update'):
    team_id: int


class TeamDeleteAskForConfirmationCallbackData(
    CallbackData,
    prefix='team-delete-ask-for-confirmation',
):
    team_id: int
