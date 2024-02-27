from views.base import View
from models import CurrentWeatherResponse


class WeatherView(View):

    def __init__(self, current_weather: CurrentWeatherResponse):
        self.__current_weather = current_weather

    def get_text(self) -> str:
        pass
