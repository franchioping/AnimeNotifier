import json

import discord

from api.anime import Anime

from managers.anime_manager import AnimeManager
from managers.user_manager import UserManager
import os


class GuildManager:
    def __init__(self, client: discord.Client, guild_id: int, anime_file_name: str = "anime.json",
                 users_file_name: str = "users.json",
                 guild_file_name: str = "guild.json"):
        self.client = client
        self.guild = self.client.get_guild(guild_id)

        self.a_man = AnimeManager(anime_file_name)
        self.u_man = UserManager(users_file_name)

        self.guild_file_name = guild_file_name

        self.anime_data = {}
        self.anime_category_id = -1
        self.load()
        self.anime_category: discord.CategoryChannel = discord.utils.get(
            self.guild.categories,
            id=self.anime_category_id
        )

    async def create_anime_role(self, name: str):
        return await self.guild.create_role(name=name)

    async def create_anime_channel(self, name: str, role: discord.Role) -> discord.TextChannel:
        channel = await self.guild.create_text_channel(name, category=self.anime_category)
        await channel.set_permissions(self.guild.default_role,
                                      overwrite=discord.PermissionOverwrite(send_messages=False, view_channel=False))
        await channel.set_permissions(role, overwrite=discord.PermissionOverwrite(view_channel=True))

        return channel

    async def add_anime_to_user(self, anime: Anime, user: discord.User):
        if not self.check_anime_in_guild(anime.id):
            await self.add_anime(anime)

        self.u_man.get_user(user.id).add_anime(anime)
        self.u_man.dump()

    async def add_anime(self, anime: Anime):
        self.a_man.add_anime(anime)

        role = await self.create_anime_role(anime.title)
        channel = await self.create_anime_channel(anime.title, role)

        self.anime_data[str(anime.id)] = {
            "channel": channel.id,
            "role": role.id
        }
        self.dump()

    def check_anime_in_guild(self, anime_id: int):
        return str(anime_id) in self.anime_data

    def get_anime_channel(self, anime_id: int):
        return self.anime_data[str(anime_id)]["channel"]

    def get_anime_role(self, anime_id: int):
        return self.anime_data[str(anime_id)]["role"]

    def load(self):
        if os.path.exists(self.guild_file_name):
            with open(self.guild_file_name, "r") as f:
                data = json.load(f)
                self.anime_data = data["anime_data"]
                self.anime_category_id = data["anime_category_id"]
        else:
            with open(self.guild_file_name, "w") as f:
                json.dump({"anime_category_id": 0, "anime_data": {}}, f)

    def dump(self):
        with open(self.guild_file_name, "r") as f:
            data = json.load(f)
        with open(self.guild_file_name, "w") as f:
            data["anime_data"] = self.anime_data
            data["anime_category_id"] = self.anime_category_id
            json.dump(data, f, indent=4)
