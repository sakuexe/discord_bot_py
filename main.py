# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
# own files
from my_commands import pokemon
from my_commands.convert_image import convert_images, fetch_images

load_dotenv()
SECRET_TOKEN: str = getenv("TOKEN") or ""
GUILD_ID: str = getenv("GUILD") or ""
GUILD = discord.Object(id=GUILD_ID)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)
tree = discord.app_commands.CommandTree(client)


async def send_message(message, sent_msg: str) -> None:
    await message.channel.send(sent_msg)


@client.event
async def on_ready():
    await tree.sync(guild=GUILD)
    print(f'We have logged in as {client.user}')


@tree.command(guild=GUILD)
async def random_pokemon(interaction):
    """Get a random pokemon"""
    assigned_pokemon = pokemon.get_random_pokemon()
    await interaction.response.send_message(f'You got: {assigned_pokemon}')


@tree.command(guild=GUILD)
async def convert_img(interaction: discord.Interaction, format: str):
    """Command for converting images to desired formats"""
    urls = await fetch_images(interaction)
    converted_images = await convert_images(urls, format)
    try:
        await interaction.response.send_message(f'here are the files', files=converted_images)
    except discord.errors.NotFound as err:
        print(err)
        await interaction.response.send_message('404, Interaction is no longer available. Try again')
    except Exception as err:
        print(err)
        await interaction.response.send_message(f'no image attachments were found from last message')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


@bot.command()
async def convert(ctx):
    """conversion command for converting images to .png"""
    await ctx.send('Ready to convert')

client.run(SECRET_TOKEN)
# bot.run(SECRET_TOKEN)
