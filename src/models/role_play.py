from pydantic import BaseModel, field_validator

__all__ = ('RolePlayAction',)


class RolePlayAction(BaseModel):
    triggers: set[str]
    emoji: str
    action_template: str

    @field_validator('action_template')
    @classmethod
    def action_must_contain_placeholders(cls, v: str) -> str:
        if '{of_user_full_name}' not in v or '{to_user_full_name}' not in v:
            raise ValueError(
                'Must contain {of_user_full_name}'
                ' and {to_user_username} placeholder'
            )
        return v
