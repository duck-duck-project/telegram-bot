import asyncio
from typing import NewType

import cloudinary.uploader

__all__ = ('upload_photo_to_cloud',)

Url = NewType('Url', str)


async def upload_photo_to_cloud(url: str) -> Url:
    uploaded_media = await asyncio.to_thread(cloudinary.uploader.upload, url)
    return Url(uploaded_media['url'])
