import cloudscraper
import bs4 as bs4
import json
from api import anime

from globals import *

cld = cloudscraper.create_scraper()


class AnimeAPI:

    @staticmethod
    def search(anime_name: str, length: int = 30) -> list[anime.Anime]:
        """
        use the sites built-in search to look for anime

        :param length: how many results do ypu want. max is 30
        :param anime_name: anime name to search, doesn't need to be exact, as this will return best matches
        :return: list of instances of anime.Anime class
        """

        req = cld.get("https://9animetv.to/search", params={"keyword": "rent a girlfriend"})

        soup = bs4.BeautifulSoup(req.text, features="html.parser")

        poster_list = soup.find(
            "div", {"id": "wrapper"}).find(
            "div", {"id": "main-wrapper"}).find(
            "div", {"class": "container"}).find(
            "div", {"id": "main-content"}).find(
            "section", {"class": "block_area block_area-anime none-bg"}).find(
            "div", {"class": "block_area-content block_area-list film_list film_list-grid"}).find(
            "div", {"class": "film_list-wrap"}).find_all(
            "div", {"class": "flw-item item-qtip"}
        )

        return [anime.Anime(int(x["data-id"])) for x in poster_list]
