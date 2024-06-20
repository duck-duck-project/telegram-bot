from pydantic import BaseModel

__all__ = ('SportActivity',)


class SportActivity(BaseModel):
    name: str
    emoji: str | None
    energy_cost_value: int
    health_benefit_value: int
    cooldown_in_seconds: int
