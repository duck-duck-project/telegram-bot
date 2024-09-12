class ApplicationError(Exception):

    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail

    def __repr__(self):
        return self.detail
