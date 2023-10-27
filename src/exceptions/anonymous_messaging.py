from dataclasses import dataclass

__all__ = ('UnsupportedContentTypeError',)


@dataclass(frozen=True, slots=True)
class UnsupportedContentTypeError(Exception):
    content_type: str

    def __str__(self) -> str:
        return f'Unsupported content type: {self.content_type}'
