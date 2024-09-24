class UserHasNoRelationshipError(Exception):
    pass


class UserHasActiveRelationshipError(Exception):

    def __init__(self, detail: str, user_id: int):
        super().__init__(detail)
        self.user_id = user_id
