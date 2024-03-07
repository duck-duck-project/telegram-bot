from aiogram.types import Message

from services.role_play_actions import RolePlayActions

__all__ = ('role_play_trigger_filter',)


def role_play_trigger_filter(
        message: Message,
        role_play_actions: RolePlayActions,
) -> dict | bool:
    role_play_action = role_play_actions.get_action(message)
    if role_play_action is not None:
        return {'role_play_action': role_play_action}
    return False
