from typing import Final

from models import MinedResourceResult
from views import MinedResourcePhotoView, MinedResourceView

__all__ = (
    'RESOURCE_NAME_TO_PHOTO_URL',
    'get_mined_resource_view'
)

RESOURCE_NAME_TO_PHOTO_URL: Final[dict[str, str]] = {
    'Уголь': 'https://i.imgur.com/FEAK3Bk.jpeg',
    'Медь': 'https://i.imgur.com/XYTcGD4.jpeg',
    'Алмаз': 'https://i.imgur.com/05vupoQ.jpeg',
    'Золото': 'https://i.imgur.com/j9Ts1wX.jpeg',
    'Железо': 'https://i.imgur.com/yc3TccG.jpeg',
    'Платина': 'https://i.imgur.com/UljsXJW.jpeg',
    'Редкоземельные металлы': 'https://i.imgur.com/NOsKJBO.jpeg',
    'Серебро': 'https://i.imgur.com/DcViaqj.jpeg',
    'Олово': 'https://i.imgur.com/CD58Qnk.jpeg',
    'Уран': 'https://i.imgur.com/IKp2D5C.jpeg',
    'Никель': 'https://i.imgur.com/VI4oIk5.jpeg',
}


def get_mined_resource_view(
        mined_resource: MinedResourceResult,
) -> MinedResourceView | MinedResourcePhotoView:
    photo_url = RESOURCE_NAME_TO_PHOTO_URL.get(mined_resource.resource_name)

    if photo_url is None:
        return MinedResourceView(mined_resource)

    return MinedResourcePhotoView(mined_resource, photo_url)
