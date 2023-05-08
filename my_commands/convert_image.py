import discord
from scripts.image_process import convert_image
from typing import List


async def fetch_images(interaction: discord.Interaction) -> List[str]:
    """Fetch the image attachments of the requesting user"""
    attachments = []
    urls: List[str] = []
    try:
        # get the last message of the user that made command
        async for message in interaction.channel.history(limit=10):
            if message.author == interaction.user:
                attachments = message.attachments
                break
        for attachment in attachments:
            urls.append(attachment.url)
    except Exception as err:
        print(err)
    return urls


async def convert_images(urls, format):
    """Download and convert the images of a given url, return a list of discord.Files"""
    converted_images = []
    try:
        for index, url in enumerate(urls):
            converted_img = convert_image(url, format)
            filename = f'image-{index}.{format}'
            file = discord.File(converted_img, filename=filename)
            converted_images.append(file)
    except Exception as err:
        print(err)
    return converted_images
