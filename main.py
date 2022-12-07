import api.anime_api as ani_api
import animeManager
import os

if __name__ == "__main__":
    ani_m = animeManager.AnimeManager(os.getcwd() + "/anime.json")
    ani_m.add_anime(ani_api.AnimeAPI.search("Rent-a-Girlfriend")[1])
