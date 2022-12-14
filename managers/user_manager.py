from managers.anime_manager import *
import os
import sys


class AnimeUser:
    def __init__(self, id: int, anime_id_list: list[int]):
        self.id: int = id
        self.anime_id_list: list[int] = anime_id_list

    def get_anime_list(self, a_man: AnimeManager) -> list[Anime]:
        ret = []
        for ani_id in self.anime_id_list:
            ret.append(a_man.get_anime_from_id(ani_id))
        return ret

    def add_anime(self, a: Anime):
        self.anime_id_list.append(a.id)

    def remove_anime(self, a: Anime):
        self.anime_id_list.remove(a.id)

    def add_anime_id(self, id: int):
        self.anime_id_list.append(id)

    def remove_anime_id(self, id: int):
        self.anime_id_list.remove(id)

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(user_dict):
        return AnimeUser(user_dict["id"], user_dict["anime_id_list"])


class UserManager:
    def __init__(self, file_name: str):
        self.file_name: str = file_name
        print(f"Starting UserManager with FilePath: {self.file_name}")
        sys.stdout.flush()
        self.user_list: list[AnimeUser] = []
        self.load()

    def reset(self):
        os.remove(self.file_name)

    def load(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as f:
                obj = json.load(f)
                for user in obj["users"]:
                    self.user_list.append(AnimeUser.from_dict(user))
        else:
            with open(self.file_name, "w") as f:
                json.dump({"users": []}, f, indent=4)

    def dump(self):
        user_dict_list = []
        for user in self.user_list:
            user_dict_list.append(user.to_dict())

        with open(self.file_name, "r") as f:
            data = json.load(f)
            data["users"] = user_dict_list

        with open(self.file_name, "w") as f:
            json.dump(data, f, indent=4)

    def add_user(self, user: AnimeUser) -> AnimeUser:
        self.user_list.append(user)
        self.dump()
        return user

    def get_user(self, id: int) -> AnimeUser:
        for user in self.user_list:
            if user.id == id:
                return user
        new_user = AnimeUser(id, [])
        self.add_user(new_user)
        return new_user
