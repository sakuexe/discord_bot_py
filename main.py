# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from textwrap import dedent
import time
# own files
from my_commands import pokemon
from my_commands.convert_image import convert_images, fetch_urls
from scripts.image_process import remove_bg
# import Raino as a client
from scripts.collections import Raino

load_dotenv()
SECRET_TOKEN: str = getenv("TOKEN") or ""
GUILD_ID: str = getenv("GUILD") or ""
GUILD: discord.Object = discord.Object(id=GUILD_ID)
INACTIVE: discord.Activity = discord.Activity(
    type=discord.ActivityType.watching, name="his rocks")

intents = discord.Intents.default()
intents.message_content = True

client = Raino(
    intents=intents, activity=INACTIVE, status=discord.Status.idle)
bot = commands.Bot(command_prefix="!", intents=intents, activity=INACTIVE)
tree = discord.app_commands.CommandTree(client)


async def toggle_activity(name: str = '') -> None:
    """Toggle the bot's activity, based on if a name for activity is passed"""
    if name:
        active = discord.Activity(
            type=discord.ActivityType.playing, name=name)
        await client.change_presence(status=discord.Status.online, activity=active)
    else:
        await client.change_presence(status=discord.Status.idle, activity=INACTIVE)


@client.event
async def on_ready():
    await tree.sync(guild=GUILD)
    print(f'We have logged in as {client.user}')


@tree.command(guild=GUILD)
async def random_pokemon(interaction: discord.Interaction):
    """Get a random pokemon"""
    assigned_pokemon = pokemon.get_random_pokemon()
    await interaction.response.send_message(f'You got: {assigned_pokemon}')


@tree.command(guild=GUILD)
async def convert_img(interaction: discord.Interaction, format: str):
    """Command for converting images to desired formats"""
    await toggle_activity("Image Conversion")
    try:
        urls = await fetch_urls(interaction)
        converted_images = await convert_images(urls, format)
    except AttributeError as error:
        await interaction.response.send_message(f'`{error}`')
    except ValueError as error:
        await interaction.response.send_message(f'`{error}`')
    except LookupError as error:
        await interaction.response.send_message(f'`{error}`')
    except discord.errors.NotFound as err:
        print(err)
        await interaction.response.send_message('`404, Interaction is no longer available. Try again`')
    except Exception as error:
        print(f'{error.__class__.__name__}: error')
        await interaction.response.send_message('`Unknown error occured`')
    else:
        # if everything works as expected
        await interaction.response.send_message(f'here are the files', files=converted_images)
    # change activity back to idle
    await toggle_activity()


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith('!rocks'):
        await toggle_activity('Counting rocks')
        await message.add_reaction('🤔')
        time.sleep(3)
        await message.channel.send(f'I currently hold onto {client.rocks} rocks')
        await toggle_activity()

    if message.content.startswith('!show rock'):
        display_rock = client.fetch_random_rock()
        rock_info = dedent(f"""
        Rock: {display_rock['name']}
        Description: {display_rock['description']}
        """)
        await message.channel.send(rock_info)
        await message.channel.send(display_rock['image'])


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    """Event for when a reaction is added to a message"""
    if reaction.message.author == client.user and reaction.emoji == '🪨':
        client.rocks += 1
        await reaction.message.add_reaction('❤️')
        await reaction.message.add_reaction('🦏')
    else:
        print(f'{user} reacted to {reaction.message.author} with {reaction.emoji}')


client.run(SECRET_TOKEN)
