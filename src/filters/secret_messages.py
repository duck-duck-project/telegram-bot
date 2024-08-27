from aiogram.types import ChosenInlineResult, InlineQuery

__all__ = (
    'secret_message_valid_format_chosen_inline_result_filter',
    'secret_message_text_length_filter',
)


def secret_message_text_length_filter(inline_query: InlineQuery) -> bool | dict:
    if 0 < len(inline_query.query) <= 200:
        return {'text': inline_query.query}
    return False


def secret_message_valid_format_chosen_inline_result_filter(
        chosen_inline_result: ChosenInlineResult,
) -> bool | dict:
    try:
        _, contact_id = chosen_inline_result.result_id.rstrip('?').split('@')
        return {'contact_id': int(contact_id)}
    except ValueError:
        return False
