import requests as r
import json
import bs4
import cloudscraper

from globals import *

cld = cloudscraper.create_scraper()


class Anime:
    def __init__(self, id: int, ep_count=-1):
        self.id = int(id)

        self.title = self.get_title()
        self.url = self.get_url()
        self.img_url = self.get_image_url()

        self.ep_count = int(ep_count)

    def _get_qtip(self):
        text = cld.get(INFO_URL + str(self.id)).text

        return bs4.BeautifulSoup(text, features="html.parser")

    def get_title(self) -> str:
        soup = self._get_qtip()
        return soup.find("div", {"class": "pre-qtip-content"}).find(
            "div", {"class": "pre-qtip-title"}).text

    def get_url(self) -> str:
        soup = self._get_qtip()
        return soup.find("div", {"class": "pre-qtip-content"}).find(
            "div", {"class": "pre-qtip-button"}).find(
            "a", {"class": "btn btn-block btn-play"}
        )["href"]

    def get_image_url(self) -> str:
        req = cld.get(BASE_URL + self.url)
        soup = bs4.BeautifulSoup(req.text, features="html.parser")
        return soup.find("div", {"id": "wrapper"}).find(
            "div", {"id": "main-wrapper"}).find(
            "div", {"class": "container"}).find(
            "div", {"id": "main-content"}).find(
            "div", {"id": "watch-block"}).find(
            "div", {"class": "player-wrap"}).find(
            "div", {"class": "wb_-playerarea"}).find(
            "div", {"class": "wb__-cover"})["style"].split(
            "(")[1][:-1]

    def get_latest_episode(self) -> int:
        soup = self._get_qtip()

        elem = soup.find("div", {"class": "pre-qtip-content"}).find("div", {"class": "pre-qtip-detail"})
        elem = elem.find("span", {"class": "pqd-li"})
        return int(elem.text.replace("\n", "").replace(" ", "").replace("Episode", "").split("/")[0])

    def get_description(self) -> str:
        req = cld.get(BASE_URL + self.url)
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
        return Anime(json_dct["id"], json_dct["ep_count"])

    def to_dict(self):
        return self.__dict__
