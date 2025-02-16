import uuid
from pathlib import Path
import importlib
pin_dl = importlib.import_module('pinterest-downloader')

extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.mp4', '.mkv', '.webp', '.svg', '.m4a', '.mp3', '.flac', '.m3u8', '.wmv', '.webm', '.mov', '.flv', '.m4v', '.ogg', '.avi', '.wav', '.apng', '.avif']

def download_link(link):
    req_id = uuid.uuid4().hex
    download_dir = '/tmp/images_' + req_id
    pin_dl.run_library_main(link, download_dir, 0, -1, False, False, False, False, False, False, False, False, None, None, None)
    file_paths = []
    for p in Path(download_dir).glob("*"):
        if p.suffix in extensions:
            file_paths.append(str(p))
    return file_paths, download_dir
    