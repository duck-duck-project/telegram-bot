from aiogram.types import ChosenInlineResult

__all__ = ('secret_message_valid_format_chosen_inline_result_filter',)


def secret_message_valid_format_chosen_inline_result_filter(
        chosen_inline_result: ChosenInlineResult,
) -> bool | dict:
    try:
        _, recipient_id = chosen_inline_result.result_id.rstrip('?').split('@')
        return {'recipient_id': int(recipient_id)}
    except ValueError:
        return False
