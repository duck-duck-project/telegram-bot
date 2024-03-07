from aiogram.types import Message

from models import RolePlayAction
from views.base import View

__all__ = ('RolePlayActionView',)


class RolePlayActionView(View):

    def __init__(self, role_play_action: RolePlayAction, message: Message):
        self.__role_play_action = role_play_action
        self.__message = message

    def get_text(self) -> str:
        reply_to_message = self.__message.reply_to_message

        of_user_full_name = self.__message.from_user.mention_html()
        to_user_full_name = reply_to_message.from_user.mention_html()

        action_text = self.__role_play_action.action_template.format(
            of_user_full_name=of_user_full_name,
            to_user_full_name=to_user_full_name,
        )
        return f'{self.__role_play_action.emoji} | {action_text}'
