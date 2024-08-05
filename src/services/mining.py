from typing import Final

from models import MinedResourceResult
from views import MinedResourcePhotoView, MinedResourceView

__all__ = (
    'RESOURCE_NAME_TO_PHOTO_URL',
    'get_mined_resource_view'
)

RESOURCE_NAME_TO_PHOTO_URL: Final[dict[str, str]] = {
    'Алмаз': 'https://i.imgur.com/05vupoQ.jpeg',
    'Золото': 'https://i.imgur.com/j9Ts1wX.jpeg',
    'Платина': 'https://i.imgur.com/UljsXJW.jpeg',
    'Уран': 'https://i.imgur.com/IKp2D5C.jpeg',
}


def get_mined_resource_view(
        mined_resource: MinedResourceResult,
) -> MinedResourceView | MinedResourcePhotoView:
    photo_url = RESOURCE_NAME_TO_PHOTO_URL.get(mined_resource.resource_name)

    if photo_url is None:
        return MinedResourceView(mined_resource)

    return MinedResourcePhotoView(mined_resource, photo_url)
