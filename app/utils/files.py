from pathlib import Path

from app.settings import MEDIA_ROOT


def get_media_dir(nested_path=""):
    return Path(MEDIA_ROOT, nested_path)
