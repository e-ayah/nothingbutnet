import os

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


def upload_video(path: str) -> str:
    result = cloudinary.uploader.upload(
        path,
        resource_type="video",
        folder="nothingbutnet",
    )
    return result["secure_url"]
