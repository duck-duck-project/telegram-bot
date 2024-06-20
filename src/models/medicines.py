from pydantic import BaseModel

__all__ = ('Medicine',)


class Medicine(BaseModel):
    name: str
    emoji: str | None
    price: int
    health_benefit_value: int
