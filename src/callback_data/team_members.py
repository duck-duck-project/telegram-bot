from aiogram.filters.callback_data import CallbackData

__all__ = (
    'TeamMemberCreateCallbackData',
    'TeamMemberDetailCallbackData',
    'TeamMemberDeleteCallbackData',
    'TeamMemberListCallbackData',
    'TeamMemberCreateAcceptInvitationCallbackData',
)


class TeamMemberDetailCallbackData(CallbackData, prefix='team-member-detail'):
    team_member_id: int


class TeamMemberDeleteCallbackData(CallbackData, prefix='team-member-delete'):
    team_member_id: int


class TeamMemberListCallbackData(CallbackData, prefix='team-member-list'):
    team_id: int


class TeamMemberCreateCallbackData(CallbackData, prefix='team-member-create'):
    team_id: int


class TeamMemberCreateAcceptInvitationCallbackData(
    CallbackData,
    prefix='team-member-create-accept-invitation',
):
    team_id: int
