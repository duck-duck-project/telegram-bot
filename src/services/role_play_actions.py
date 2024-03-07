from collections.abc import Iterable

from aiogram.types import Message

from models import RolePlayAction

__all__ = ('RolePlayActions',)


class RolePlayActions:

    def __init__(self, role_play_actions: Iterable[RolePlayAction]):
        self.role_play_actions = tuple(role_play_actions)

    def get_action(self, message: Message) -> RolePlayAction | None:
        message_text = message.text.lower()
        for role_play_action in self.role_play_actions:
            for trigger in role_play_action.triggers:
                if trigger in message_text:
                    return role_play_action
