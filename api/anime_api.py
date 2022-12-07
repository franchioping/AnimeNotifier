import requests as r
import bs4 as bs4
import json
from api import anime

from globals import *


class AnimeAPI:

    @staticmethod
    def search(anime_name: str) -> list[anime.Anime]:
        """
        use the sites built-in search to look for anime

        :param anime_name: anime name to search, doesn't need to be exact, as this will return best matches
        :return: list of instances of anime.Anime class
        """

        request = r.get(SEARCH_URL + anime_name)
        parsed = bs4.BeautifulSoup(request.text, features="html.parser")
        list_div = parsed.find("div", {"class": "film_list-wrap"})
        item_list = list_div.find_all("div", {"class": "flw-item item-qtip"})

        ret = []
        for i in item_list:
            # Here's an example of what "i" looks like
            """
            <div class="flw-item item-qtip" data-id="100" data-hasqtip="1" aria-describedby="qtip-1">
                <div class="film-poster">
                    <div class="tick-item tick-quality">HD</div>
                    <div class="tick ltr">

                            <div class="tick-item tick-sub">SUB</div>


                            <div class="tick-item tick-dub">DUB</div>

                    </div>

                    <div class="tick rtl">
                        <div class="tick-item tick-eps">

                                Ep 1043

                        </div>
                    </div>

                    <img data-src="https://img.bunnycdnn.ru/_r/300x400/100/54/90/5490cb32786d4f7fef0f40d7266df532/5490cb32786d4f7fef0f40d7266df532.jpg" class="film-poster-img lazyloaded" alt="One Piece" src="https://img.bunnycdnn.ru/_r/300x400/100/54/90/5490cb32786d4f7fef0f40d7266df532/5490cb32786d4f7fef0f40d7266df532.jpg">
                    <a href="/watch/one-piece-100" class="film-poster-ahref"><i class="fas fa-play"></i></a>
                </div>
                <div class="film-detail">
                    <h3 class="film-name">
                        <a href="/watch/one-piece-100" title="One Piece" class="dynamic-name" data-jname="One Piece">One Piece</a>
                    </h3>
                </div>
                <div class="clearfix"></div>
            </div>
            """

            film_detail = i.find_next("div", {"class": "film-detail"})

            # <h3 class="film-name"> DYNAMIC_NAME (see under) </h3>
            film_name = film_detail.find_next("h3", {"class": "film-name"})

            # <a href="/watch/one-piece-100" title="One Piece" class="dynamic-name" data-jname="One Piece">One Piece</a>
            dynamic_name = film_name.find("a", {"class": "dynamic-name"})

            title = dynamic_name["title"]
            url = dynamic_name["href"]
            anime_id = int(i["data-id"])

            a = anime.Anime(title, anime_id, url)
            ret.append(a)
        return ret
