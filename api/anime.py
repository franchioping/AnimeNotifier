import requests as r
import json
import bs4
import cloudscraper

from globals import *


class Anime:
    def __init__(self, title: str, id: int, url: str, img_url: str, ep_count=-1):
        self.title = str(title)
        self.id = int(id)
        self.url = str(url)
        self.img_url = img_url
        self.ep_count = int(ep_count)
        self.cld = cloudscraper.create_scraper()

    def get_latest_episode(self) -> int:
        text = self.cld.get(f"https://9animetv.to/ajax/movie/qtip/{self.id}").text

        soup = bs4.BeautifulSoup(text, features="html.parser")

        elem = soup.find("div", {"class": "pre-qtip-content"}).find("div", {"class": "pre-qtip-detail"})
        elem = elem.find("span", {"class": "pqd-li"})
        return int(elem.text.replace("\n", "").replace(" ", "").replace("Episode", "").split("/")[0])

    def get_description(self) -> str:
        req = r.get(BASE_URL + self.url)
        soup = bs4.BeautifulSoup(req.text, features="html.parser")
        return soup.find("meta", {"name": "description"})["content"]

    def check_new_episode_came_out(self) -> bool:
        if self.ep_count != self.get_ep_count():
            self.update_ep_count()
            return True
        return False

    def get_ep_count(self) -> int:
        return self.get_latest_episode()

    def update_ep_count(self) -> int:
        self.ep_count = self.get_ep_count()
        return self.ep_count

    @staticmethod
    def from_dict(json_dct):
        return Anime(json_dct["title"], json_dct["id"], json_dct["url"], json_dct["img_url"], json_dct["ep_count"])

    def to_dict(self):
        return self.__dict__
