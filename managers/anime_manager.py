import json
import os.path

from api import anime
from api.anime import Anime


class AnimeManager:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.anime_list: list[anime.Anime] = []
        self.load_data()

    def check_for_new_episodes(self, callback):
        for a in self.anime_list:
            if a.check_new_episode_came_out():
                callback(a)

    def write_data(self):
        anime_dict_list = []
        for a in self.anime_list:
            print(a.to_dict())
            anime_dict_list.append(a.to_dict())

        with open(self.file_name, "r") as f:
            data = json.load(f)
            data["anime_list"] = anime_dict_list

        with open(self.file_name, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as f:
                data = json.load(f)
                for obj in data["anime_list"]:
                    self.anime_list.append(anime.Anime.from_dict(obj))
        else:
            with open(self.file_name, "w") as f:
                json.dump({"anime_list": []}, f, indent=4)

    def add_anime(self, anim: anime.Anime) -> int:
        if self.check_if_anime_is_in_list(anim.id):
            self.anime_list.append(anim)
            self.write_data()
            return 0
        return -1

    def remove_anime(self, id: int) -> int:
        for a in self.anime_list:
            if a.id == id:
                self.anime_list.remove(a)
                return 0
        return -1

    def get_anime_from_id(self, id: int) -> Anime | None:
        for a in self.anime_list:
            if a.id == id:
                return a
        return None

    def check_if_anime_is_in_list(self, id: int) -> bool:
        for a in self.anime_list:
            if a.id == id:
                return False
        return True
