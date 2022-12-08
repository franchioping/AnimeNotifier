import requests as r
import json
import bs4

from globals import *
from api import episode


class Anime:
    def __init__(self, title: str, id: int, url: str, img_url: str, ep_count=-1):
        self.title = str(title)
        self.id = int(id)
        self.url = str(url)
        self.img_url = img_url
        self.ep_count = int(ep_count)

    def get_ep_list(self) -> list[episode.Episode]:
        """
        uses the site's own api calls to get an episode list for the anime

        :return: list of instances of episode.Episode class
        """

        ep_list_url = EPISODE_LIST_URL + str(self.id)
        request = r.get(ep_list_url)
        html = json.loads(request.text)["html"]

        parsed = bs4.BeautifulSoup(html, features="html.parser")

        # the following comment is an example of what episode_pages looks like
        episode_pages = parsed.find("div", {"class": "block_area-content"})
        """
        <div class="block_area-content">
                <div id="episodes-page-1" class="episodes-ul" data-page="1" style="">
                    <a href="/watch/rent-a-girlfriend-2037?ep=24724" title="Rent-a-Girlfriend" class="item ep-item" data-number="1" data-id="24724">
                        <div class="order">1</div>
                    </a>
                    <a href="/watch/rent-a-girlfriend-2037?ep=24725" title="Ex-Girlfriend and Girlfriend" class="item ep-item" data-number="2" data-id="24725">
                        <div class="order">2</div>
                    </a>

                    ===== THIS KEEPS ON GOING, AND SKIPS TO THE NEXT PAGE WHEN WE REACH 100 =====

                    <div class="clearfix"></div>
                </div>
        </div>    
        """

        page_tag_list = episode_pages.find_all("div", {"class": "episodes-ul"})
        ep_list = []
        for page in page_tag_list:
            eps = page.find_all("a", {"class": "item ep-item"})
            for ep in eps:
                ep_list.append(episode.Episode(ep["title"], ep["data-number"], ep["data-id"]))
        return ep_list

    def get_latest_episode(self):
        return self.get_ep_list()[-1]

    def get_description(self) -> str:
        req = r.get(BASE_URL + self.url)
        soup = bs4.BeautifulSoup(req.text,  features="html.parser")
        return soup.find("meta", {"name": "description"})["content"]

    def check_new_episode_came_out(self) -> bool:
        if self.ep_count != self.get_ep_count():
            self.update_ep_count()
            return True
        return False

    def get_ep_count(self) -> int:
        return int(self.get_ep_list()[-1].ep_num)

    def update_ep_count(self) -> int:
        self.ep_count = self.get_ep_count()
        return self.ep_count

    @staticmethod
    def from_dict(json_dct):
        return Anime(json_dct["title"], json_dct["id"], json_dct["url"], json_dct["img_url"], json_dct["ep_count"])

    def to_dict(self):
        return self.__dict__
