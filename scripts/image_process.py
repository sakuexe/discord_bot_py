from io import BytesIO
from PIL import Image
from urllib.request import urlopen, Request
from time import time


def convert_image(image_url: str, format: str):
    original_img = download_image(image_url)
    with Image.open(BytesIO(original_img)) as img:
        # convert the image to format
        buffer = BytesIO()
        img.save(buffer, format=format)
        buffer.seek(0)
        return buffer


def download_image(image_url: str):
    user_agent = f'mediamokki-convert-{time()}'
    req = Request(image_url, headers={'User-Agent': user_agent})
    with urlopen(req) as img:
        return img.read()


if __name__ == "__main__":
    # convert_image()
    print("testing image conversion")
    url = 'https://images.nintendolife.com/0c5849002e114/donkey-kong.large.jpg'
    image = convert_image(url, 'png')
