from collections.abc import Callable

from aiogram.types import Message

__all__ = ('create_name_filter',)


def create_name_filter(
        command_name: str,
        param_name: str,
) -> Callable[[Message], bool | dict]:
    def wrapper(message: Message) -> bool | dict:
        if message.text is None:
            return False

        try:
            command, name = message.text.splitlines()
        except ValueError:
            return False

        if command.lower().strip() != command_name:
            return False

        return {param_name: name}

    return wrapper
