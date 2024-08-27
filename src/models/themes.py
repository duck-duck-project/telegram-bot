from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

__all__ = ('Theme', 'ThemesPage')


class Theme(BaseModel):
    id: UUID
    secret_message_template_text: str
    secret_media_template_text: str
    secret_message_view_button_text: str
    secret_message_delete_button_text: str
    secret_message_read_confirmation_text: str
    secret_message_deleted_confirmation_text: str
    secret_message_deleted_text: str
    secret_message_missing_text: str
    created_at: datetime

    @field_validator(
        'secret_message_template_text',
        'secret_media_template_text',
        'secret_message_read_confirmation_text',
    )
    @classmethod
    def must_contain_name_placeholder(cls, v: str) -> str:
        if '{name}' not in v:
            raise ValueError('Must contain {name}')
        return v

    @field_validator('secret_message_read_confirmation_text')
    @classmethod
    def must_contain_text_placeholder(cls, v: str) -> str:
        if '{text}' not in v:
            raise ValueError('Must contain {text}')
        return v


class ThemesPage(BaseModel):
    themes: list[Theme]
    is_end_of_list_reached: bool
