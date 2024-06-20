from pydantic import BaseModel

__all__ = ('SportActivity', 'SportActivityActionResult')


class SportActivity(BaseModel):
    name: str
    emoji: str | None
    energy_cost_value: int
    health_benefit_value: int
    cooldown_in_seconds: int


class SportActivityActionResult(BaseModel):
    user_id: int
    user_energy: int
    user_health: int
    energy_cost_value: int
    sport_activity_name: str
    health_benefit_value: int
    cooldown_in_seconds: int
