import discord
from discord import app_commands
import os
from dotenv import load_dotenv

from api.anime_api import AnimeAPI

from discord_util import *

load_dotenv()

token = os.getenv("TOKEN")
assert token is not None

MY_GUILD = discord.Object(id=1042133536926347324)  # replace with your guild id


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command(name="search-anime")
@app_commands.describe(
    anime_name='Name of the anime you want to search for. standard ASCII characters only'
)
async def search_anime_command(interaction: discord.Interaction, anime_name: str):
    anime_list = AnimeAPI.search(anime_name, 10)

    view = ListAnime(anime_list)
    await interaction.response.defer()
    await interaction.followup.send("Check the bot DMs to continue")
    await interaction.user.send(view=view, embed=get_embed_for_anime(anime_list[0]))
    await view.wait()
    print(view.ret)


client.run(token)
