from io import BytesIO
from PIL import Image
from urllib.request import urlopen, Request
from discord import File
from time import time
# extra plugin that allows for avif conversion
import pillow_avif


def convert_image(image_url: str, format: str):
    original_img = download_image(image_url)
    img = Image.open(BytesIO(original_img))
    try:
        # convert the image to format
        buffer = BytesIO()
        if format.lower() == 'jpeg':
            background = Image.new('RGBA', img.size, (255, 255, 255))
            alpha = Image.alpha_composite(background, img)
            img = alpha.convert("RGB")
        img.save(buffer, format=format)
        buffer.seek(0)
    except KeyError as error:
        print('KeyError:', error)
        raise KeyError(f'No format "{format}" available to convert to')
    except ValueError as error:
        print("ValueError:", error)
        raise ValueError(
            f'Could not convert image to {format}. (try converting to another format first)')
    return buffer


def download_image(image_url: str):
    """Download image from an URL, return the image as bytes"""
    user_agent = f'mediamokki-convert-{time()}'
    req = Request(image_url, headers={'User-Agent': user_agent})
    with urlopen(req) as request:
        return request.read()


def remove_bg(image_url: str):
    original_img = download_image(image_url)
    img = Image.open(BytesIO(original_img))
    # remove background
    buffer = BytesIO()
    img.save(buffer, format='png')
    buffer.seek(0)
    return File(buffer, filename='removed_bg.png')


if __name__ == "__main__":
    # convert_image()
    print("testing image conversion")
    url = 'https://images.nintendolife.com/0c5849002e114/donkey-kong.large.jpg'
    image = convert_image(url, 'png')
