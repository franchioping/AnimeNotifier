import api.anime_api as ani_api
import animeManager

if __name__ == "__main__":
    ani_m = animeManager.AnimeManager("anime.json")
    ani_m.anime_list.append(ani_api.AnimeAPI.search("Rent-a-Girlfriend")[1])
    ani_m.write_data()
