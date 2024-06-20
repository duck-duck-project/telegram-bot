class FoodItemDoesNotExistError(Exception):

    def __init__(self, food_item_name: str):
        super().__init__('Food item does not exist')
        self.food_item_name = food_item_name
