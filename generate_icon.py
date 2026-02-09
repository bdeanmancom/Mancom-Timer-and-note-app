"""
Download a logo (GIF/PNG) and generate icon.ico for the app.
Usage:
    python generate_icon.py <url>

Saves: icon.ico and icon.png
"""
import sys
import io
from pathlib import Path
try:
    from urllib.request import urlopen
except Exception:
    urlopen = None

from PIL import Image

def download_image(url):
    if url.startswith("http://") or url.startswith("https://"):
        resp = urlopen(url)
        data = resp.read()
        return io.BytesIO(data)
    else:
        return open(url, "rb")


def make_icon(input_stream, out_icon_path="icon.ico", out_png_path="icon.png"):
    img = Image.open(input_stream)
    # If animated GIF, take first frame
    try:
        img.seek(0)
    except Exception:
        pass
    img = img.convert("RGBA")

    # Resize to square while keeping aspect ratio and center on transparent background
    size = (256, 256)
    img.thumbnail(size, Image.LANCZOS)
    background = Image.new("RGBA", size, (0,0,0,0))
    offset = ((size[0] - img.width) // 2, (size[1] - img.height) // 2)
    background.paste(img, offset, img)

    # Save png preview
    background.save(out_png_path, format="PNG")

    # Save as multi-size ICO
    sizes = [(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)]
    icon_sizes = [s for s in sizes if s[0] <= background.width]
    background.save(out_icon_path, format="ICO", sizes=icon_sizes)
    return out_icon_path, out_png_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_icon.py <url-or-local-path>")
        sys.exit(1)
    url = sys.argv[1]
    print("Downloading:", url)
    try:
        stream = download_image(url)
    except Exception as e:
        print("Failed to download or open file:", e)
        sys.exit(1)

    out_icon, out_png = make_icon(stream)
    print("Generated:", out_icon, out_png)
