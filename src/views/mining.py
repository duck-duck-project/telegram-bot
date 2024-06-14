from datetime import timedelta

import humanize

from models import MinedResource
from views import View

__all__ = ('MinedResourceView', 'MiningActionThrottledView')


class MiningActionThrottledView(View):

    def __init__(self, next_mining_in_seconds: int):
        self.__next_mining_in_seconds = next_mining_in_seconds

    def get_text(self) -> str:
        next_mining = humanize.precisedelta(
            timedelta(seconds=self.__next_mining_in_seconds),
        )
        return f'❌ Следующая добыча через: {next_mining}'


class MinedResourceView(View):

    def __init__(self, mined_resource: MinedResource):
        self.__mined_resource = mined_resource

    def get_text(self) -> str:
        return (
            f'⛏️ Вы добыли ресурс "{self.__mined_resource.resource_name}"'
            f' на сумму {self.__mined_resource.wealth} монет!'
        )
