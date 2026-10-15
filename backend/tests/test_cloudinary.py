import cloudinary.uploader

from services.cloudinary import upload_video


#upload_video sends a video upload to our folder and returns the https url
#(uploader is faked so this runs without Cloudinary credentials or network)
def test_upload_video_returns_secure_url(monkeypatch):
    calls = {}

    def fake_upload(path, **kwargs):
        calls["path"] = path
        calls["kwargs"] = kwargs
        return {"secure_url": "https://res.cloudinary.com/demo/video/upload/clip.mp4"}

    monkeypatch.setattr(cloudinary.uploader, "upload", fake_upload)

    url = upload_video("clip.mp4")

    assert url == "https://res.cloudinary.com/demo/video/upload/clip.mp4"
    assert calls["path"] == "clip.mp4"
    assert calls["kwargs"]["resource_type"] == "video"
    assert calls["kwargs"]["folder"] == "nothingbutnet"
