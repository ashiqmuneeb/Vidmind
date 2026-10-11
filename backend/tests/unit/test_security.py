from backend.app.core.security import is_valid_youtube_url, sanitize_filename
from backend.app.core.config import settings


def test_is_valid_youtube_url():
    valid_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/shorts/dQw4w9WgXcQ",
    ]
    for url in valid_urls:
        assert is_valid_youtube_url(url) is True

    invalid_urls = [
        "https://example.com/video.mp4",
        "https://notyoutube.com/watch?v=123",
        "invalid-url-string",
        "",
    ]
    for url in invalid_urls:
        assert is_valid_youtube_url(url) is False


def test_sanitize_filename():
    assert sanitize_filename("my:file?name<1>.mp4") == "myfilename1.mp4"
    assert sanitize_filename("  spaces  and  dots.txt ") == "spaces__and__dots.txt"
    assert sanitize_filename("") == "unnamed_video"


def test_settings_cors_list():
    assert isinstance(settings.cors_origins_list, list)
    assert len(settings.cors_origins_list) > 0
