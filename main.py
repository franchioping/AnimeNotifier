import discord
from discord import app_commands
from discord.ext import tasks
import os
from dotenv import load_dotenv

from api.anime_api import AnimeAPI

from discord_util import *
from managers.guild_manager import GuildManager

g_man: GuildManager

load_dotenv()

token = os.getenv("TOKEN")
guild = int(os.getenv("GUILD"))
assert token is not None
assert guild is not None

MY_GUILD = discord.Object(id=guild)  # replace with your guild id


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
    global g_man
    g_man = GuildManager(client, guild)
    check_for_new_manga.start()


async def list_anime_in_msg(interaction: discord.Interaction, anime_list: list[Anime]):
    view = ListAnime(anime_list)

    await interaction.followup.send("Check the bot DMs to continue")
    await interaction.user.send(view=view, embed=get_embed_for_anime(anime_list[0]))
    await view.wait()
    for action in view.ret:
        if action["action"] == 1:
            await g_man.add_anime_to_user(action["anime"], interaction.user)
        if action["action"] == -1:
            await g_man.remove_anime_from_user(action["anime"], interaction.user)


@client.tree.command(name="search-anime")
@app_commands.describe(
    anime_name='Name of the anime you want to search for. standard ASCII characters only'
)
async def search_anime_command(interaction: discord.Interaction, anime_name: str):
    await interaction.response.defer()
    anime_list = AnimeAPI.search(anime_name)
    await list_anime_in_msg(interaction, anime_list)


@client.tree.command(name="list-anime")
async def list_anime_command(interaction: discord.Interaction):
    await interaction.response.defer()
    anime_list = g_man.u_man.get_user(interaction.user.id).get_anime_list(g_man.a_man)
    await list_anime_in_msg(interaction, anime_list)


"""
@client.tree.command(name="reset_server_command")
async def reset_server_command(interaction: discord.Interaction):
    await interaction.response.defer()

    chs = g_man.anime_category.channels
    for c in chs:
        await c.delete()

    anime_list = g_man.a_man.anime_list
    anime_id_list = []
    for a in anime_list:
        anime_id_list.append(a.id)
    for id in anime_id_list:
        await g_man.get_anime_role(id).delete()

    g_man.reset()

    g_man.load()
    g_man.a_man.load()
    g_man.u_man.load()

    g_man.load()
    g_man.a_man.load()
    g_man.u_man.load()

    await interaction.followup.send("Done maybe not really IDGAF", ephemeral=True)
"""


@client.tree.command(name="set-anime-category")
async def set_anime_category_command(interaction: discord.Interaction, cat: discord.CategoryChannel):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You shouldn't be here, bye!", ephemeral=True)
    else:
        g_man.anime_category = cat
        g_man.anime_category_id = cat.id
        g_man.dump()

        await interaction.response.send_message("Done maybe idk", ephemeral=True)


@tasks.loop(seconds=300)
async def check_for_new_manga():
    await g_man.a_man.check_for_new_episodes(send_notification_message)


async def send_notification_message(anime: Anime):
    g_man.a_man.dump()
    role = g_man.get_anime_role(anime.id)
    await g_man.get_anime_channel(anime.id).send(embed=get_embed_for_episode(anime, anime.ep_count),
                                                 content=role.mention,
                                                 allowed_mentions=discord.AllowedMentions(everyone=True)
                                                 )


client.run(token)
