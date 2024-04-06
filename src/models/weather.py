from pydantic import BaseModel, Field

__all__ = (
    'GeoCoordinates',
)


class GeoCoordinates(BaseModel):
    name: str
    latitude: float = Field(alias='lat')
    longitude: float = Field(alias='lon')
    country: str
