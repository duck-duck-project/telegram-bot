from pydantic import BaseModel

__all__ = ('Medicine', 'MedicineConsumptionResult')


class Medicine(BaseModel):
    name: str
    emoji: str | None
    price: int
    health_benefit_value: int


class MedicineConsumptionResult(BaseModel):
    user_id: int
    medicine_name: str
    price: int
    health_benefit_value: int
    user_health: int
