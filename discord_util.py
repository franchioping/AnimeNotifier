import discord
from api.anime import Anime
from globals import *


class ListAnime(discord.ui.View):
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

    @discord.ui.button(label='Done', style=discord.ButtonStyle.blurple)
    async def exit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if len(self.ret) > 0:
            await interaction.response.send_message("Your list has been altered successfully", ephemeral=True)
        else:
            await interaction.response.send_message("You didn't make any changes", ephemeral=True)
        self.stop()


def get_embed_for_anime(anime: Anime) -> discord.Embed:
    e = discord.Embed(title=anime.title, description=anime.get_description(), url=BASE_URL + anime.url)
    e.set_thumbnail(url=anime.img_url)
    return e


def get_embed_for_episode(anime: Anime, ep_num: int) -> discord.Embed:
    e = discord.Embed(title=f"Episode {ep_num} of {anime.title}", description=f"Episode {ep_num} of {anime.title} anime just released!",
                      url=BASE_URL + anime.url
                      )
    e.set_thumbnail(url=anime.img_url)
    return e
