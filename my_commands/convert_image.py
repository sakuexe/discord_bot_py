import discord
from scripts.image_process import convert_image
from typing import List
from os import path

HISTORY_LIMIT = 15


async def fetch_urls(interaction: discord.Interaction) -> List[str]:
    """Fetch the image attachments of the requesting user"""
    attachments: List[discord.Attachment] = []
    urls: List[str] = []
    # get the last message of the user that made command
    async for message in interaction.channel.history(limit=HISTORY_LIMIT):
        if message.author == interaction.user:
            attachments = message.attachments
            break
    if len(attachments) == 0:
        raise AttributeError(
            f"No prior attachments from {interaction.user} was found. (Checked the last {HISTORY_LIMIT} messages)")
    for attachment in attachments:
        urls.append(attachment.url)
    return urls


async def convert_images(urls, format):
    """Download and convert the images of a given url, return a list of discord.Files"""
    converted_images = []
    for url in urls:
        # get the filename from the url, without the filetype
        original_filename = path.splitext(path.basename(url))[1]
        converted_img = convert_image(url, format)
        filename = f'{original_filename}.{format}'
        # save the converted image as a discord file and add it to the list
        file = discord.File(converted_img, filename=filename)
        converted_images.append(file)
    return converted_images
