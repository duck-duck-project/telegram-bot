from exceptions.base import ApplicationError

__all__ = ('FoodItemDoesNotExistError',)


class FoodItemDoesNotExistError(ApplicationError):

    def __init__(
            self,
            detail: str,
            food_item_name: str,
            food_item_type: int,
    ):
        super().__init__(detail)
        self.food_item_name = food_item_name
        self.food_item_type = food_item_type
