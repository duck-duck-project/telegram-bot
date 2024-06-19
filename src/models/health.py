from pydantic import BaseModel

__all__ = ('SportActivity',)


class SportActivity(BaseModel):
    name: str
    energy_cost_value: int
    health_benefit_value: int
