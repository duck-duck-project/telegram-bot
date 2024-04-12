__all__ = ('UnsupportedContentTypeError',)


class UnsupportedContentTypeError(Exception):

    def __init__(self, content_type: str):
        self.content_type = content_type

    def __str__(self) -> str:
        return f'Unsupported content type: {self.content_type}'
