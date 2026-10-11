import re
from urllib.parse import urlparse


def is_valid_youtube_url(url: str) -> bool:
    """Validates if a URL is a legitimate YouTube link."""
    if not url:
        return False
    parsed = urlparse(url)
    if parsed.netloc in ("youtube.com", "www.youtube.com", "m.youtube.com"):
        return bool(re.search(r"[?&]v=([a-zA-Z0-9_-]{11})", url) or "shorts" in parsed.path or "embed" in parsed.path)
    if parsed.netloc in ("youtu.be", "www.youtu.be"):
        return bool(re.search(r"^/([a-zA-Z0-9_-]{11})", parsed.path))
    return False


def sanitize_filename(name: str) -> str:
    """Sanitizes user input for safe filesystem storage."""
    # Strip illegal characters on Windows/Linux
    clean = re.sub(r'[\\/*?:"<>|]', "", name)
    clean = clean.strip().replace(" ", "_")
    return clean[:100] if clean else "unnamed_video"
