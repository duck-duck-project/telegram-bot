import asyncio

import cloudinary.uploader

from services.services import Url


async def upload_photo_to_cloud(url: str) -> Url:
    uploaded_media = await asyncio.to_thread(cloudinary.uploader.upload, url)
    return Url(uploaded_media['url'])
