import json
from api import anime


class AnimeManager:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.anime_list = []
        self.load_data()

    def write_data(self):
        anime_dict_list = []
        for a in self.anime_list:
            a.update_ep_count()
            print(a.to_dict())
            anime_dict_list.append(a.to_dict())

        with open(self.file_name, "r") as f:
            data = json.load(f)
            data["anime_list"] = anime_dict_list

        with open(self.file_name, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        with open(self.file_name, "r") as f:
            data = json.load(f)
            for obj in data["anime_list"]:
                self.anime_list.append(anime.Anime.from_dict(obj))
