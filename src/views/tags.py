from aiogram.types import User

from views import View

__all__ = ('TagGivenView',)


class TagGivenView(View):

    def __init__(self, to_user: User):
        self.__to_user = to_user

    def get_text(self) -> str:
        return f'✅ Тэг пользователю {self.__to_user.url} выдан'
