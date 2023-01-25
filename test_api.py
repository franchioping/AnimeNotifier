import unittest
from api import anime, anime_api
import re
import json


class TestAnime(unittest.TestCase):

    def test_anime_get_name(self):
        ani = anime.Anime(2037)
        self.assertEqual(ani.get_title(), "Rent-a-Girlfriend")

    def test_anime_get_url(self):
        ani = anime.Anime(2037)
        self.assertEqual("/watch/rent-a-girlfriend-2037", ani.get_url())

    def test_anime_get_image_url(self):
        ani = anime.Anime(2037)
        self.assertEqual(
            "https://img.bunnycdnn.ru/_r/300x400/100/62/09/6209ac54830ee3befb26d2ff148e671d/6209ac54830ee3befb26d2ff148e671d.jpg",
            ani.get_image_url())

    def test_anime_get_description(self):
        ani = anime.Anime(2037)
        original_desc = """Kazuya Kinoshita is a 20-year-old college student who has a wonderful girlfriend: the bright and sunny Mami Nanami. But suddenly, he doesn't. Without warning, Mami breaks up with him, leaving him utterly heartbroken and lonely. Seeking to soothe the pain, he hires a rental girlfriend through an online app. His partner is Chizuru Mizuhara, who through her unparalleled beauty and cute demeanor, manages to gain Kazuya's affection. But after reading similar experiences other customers had had with Chizuru, Kazuya believes her warm smile and caring personality were all just an act to toy with his heart, and he rates her poorly. Aggravated, Chizuru lambastes him for his shameless hypocrisy, revealing her true pert and hot-tempered self. This one-sided exchange is cut short, however, when Kazuya finds out that his grandmother has collapsed. They dash toward the hospital and find Kazuya's grandmother already in good condition. Baffled by Chizuru's presence, she asks who this girl might be. On impulse, Kazuya promptly declares that they are lovers, forcing Chizuru to play the part. But with Kazuya still hung up on his previous relationship with Mami, how long can this difficult client and reluctant rental girlfriend keep up their act? [Written by MAL Rewrite]"""
        result = ani.get_description().replace("\r\n", "").replace("\n", "")
        self.assertEqual(original_desc.replace(" ", ""), result.replace(" ", ""))

    def test_anime_jsonify(self):
        ani = anime.Anime(2037)
        jsn = json.dumps(ani.to_dict())
        self.assertIsNotNone(jsn)

    def test_anime_get_ep(self):
        ani = anime.Anime(2037)
        self.assertEqual(12, ani.get_ep_count())


class TestAnimeApi(unittest.TestCase):

    def test_search_anime(self):
        ani_list = anime_api.AnimeAPI.search("rent a gf")
        for ani in ani_list:
            self.assertIsNotNone(ani)


if __name__ == "__main__":
    unittest.main()
