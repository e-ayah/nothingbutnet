import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.cloudinary import upload_video

TEST_CLIP = os.path.join(os.path.dirname(__file__), "test_clip.mp4")

if __name__ == "__main__":
    print(f"Uploading {TEST_CLIP} ...")
    url = upload_video(TEST_CLIP)
    print(f"Uploaded! Video URL: {url}")

