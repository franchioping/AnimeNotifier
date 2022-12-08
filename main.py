from typing import Optional

import discord
from discord import app_commands
from discord import ui
import os
from dotenv import load_dotenv
from api.anime_api import AnimeAPI
from api.anime import *

load_dotenv()

token = os.getenv("TOKEN")
assert token is not None

MY_GUILD = discord.Object(id=1042133536926347324)  # replace with your guild id


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


def get_embed_for_anime(anime: Anime) -> discord.Embed:
    e = discord.Embed(title=anime.title, description=anime.get_description())
    e.set_thumbnail(url=anime.img_url)
    return e


# Define a simple View that gives us a confirmation menu
class Confirm(discord.ui.View):
    def __init__(self, anime_list: list[Anime]):
        super().__init__()
        self.ret = []
        self.index = 0
        self.anime_list = anime_list

    async def print_anime(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.message.edit(embed=get_embed_for_anime(self.anime_list[self.index]))

    @discord.ui.button(label='Prev', style=discord.ButtonStyle.grey)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index > 0:
            self.index -= 1

        await self.print_anime(interaction)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.grey)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index < len(self.anime_list):
            self.index += 1

        await self.print_anime(interaction)

    @discord.ui.button(label='Add', style=discord.ButtonStyle.green)
    async def add(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.ret.append({"anime": self.anime_list[self.index], "action": 1})

    @discord.ui.button(label='Remove', style=discord.ButtonStyle.red)
    async def remove(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.ret.append({"anime": self.anime_list[self.index], "action": -1})

    @discord.ui.button(label='Exit', style=discord.ButtonStyle.red)
    async def exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Anime added to your list successfully", ephemeral=True)
        self.stop()


@client.tree.command(name="search-anime")
@app_commands.describe(
    anime_name='Name of the anime you want to search for. standard ASCII characters only'
)
async def search_anime_command(interaction: discord.Interaction, anime_name: str):
    """Adds two numbers together."""

    anime_list = AnimeAPI.search(anime_name, 10)
    names_str = ""
    for i in range(len(anime_list)):
        names_str += f"{i}: " + anime_list[i].title + "\n"

    view = Confirm(anime_list)
    await interaction.response.defer()
    await interaction.followup.send(view=view, embed=get_embed_for_anime(anime_list[0]), ephemeral=True)
    await view.wait()
    print(view.ret)


client.run(token)
