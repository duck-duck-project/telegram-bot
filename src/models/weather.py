from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from pydantic import BaseModel

__all__ = (
    'Location',
    'CurrentWeather',
    'CurrentWeatherResponse',
)


class Location(BaseModel):
    name: str
    region: str
    country: str
    latitude: Decimal
    longitude: Decimal
    localtime: datetime
    timezone: str


class CurrentWeather(BaseModel):
    last_updated: datetime
    temperature_celsius: Decimal
    feels_like_celsius: Decimal
    wind_speed_kilometers_per_hour: Decimal
    wind_direction: str
    humidity_percent: int
    cloud_cover_percent: int
    uv_index: Decimal


class CurrentWeatherResponse(BaseModel):
    location: Location
    current: CurrentWeather
