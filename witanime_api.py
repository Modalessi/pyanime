import requests
import re
from bs4 import BeautifulSoup
from bs4 import element
from selenium_handler import SeleniumHandler
from website_api_interface import WebsiteAPIInterface
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By



class WitAnimeAPI(WebsiteAPIInterface) :


    WEBSITE_NAME = "WitAnime"

    BASE_URL = "https://witanime.rest"

    @staticmethod
    def search(query: str) -> list:
        '''
        search for a query in the website and return results in a list of dicts
        with the following format
        {
            "title of the result" : str
            "link" : str
        }
        '''

        result_page = requests.get(WitAnimeAPI.BASE_URL, params={"search_param" : "animes", "s": query}, timeout=1000)
        print("link", result_page.url)
        print("result page", result_page)
        soup = BeautifulSoup(result_page.text, features="lxml")

        anime_list_div = soup.find("div", class_ = "anime-list-content")
        animes_div = anime_list_div.find_all("div", class_ = "col-lg-2 col-md-4 col-sm-6 col-xs-6 col-no-padding col-mobile-no-padding")
        for anime_div in animes_div :
            print(anime_div.h3.a.string)





    @staticmethod
    def is_movie(link: str) -> bool:
        '''
        return wether the webpage link is a movie or not
        '''

    @staticmethod
    def contains_seasons(link: str) -> bool:
        '''
        return wether the webpage contains seasons or not
        '''

    @staticmethod
    def get_seasons(link: str) -> list:
        '''
        should return all seasons in a an array of dicts
        with the following format
        {
            "title of the season" : str
            "link" : str
            "index" : int
        }
        '''

    @staticmethod
    def get_episodes(link: dict) -> list:
        '''
        should return all episodes in a an array of dicts
        with the following format
        {
            "title of the episode" : str
            "link" : str
            "index" : int
        }
        '''

    @staticmethod
    def get_m3u8_link(link: dict) -> str:
        '''
        should return m3u8 link for an episode or a movie
        in order to pass to a media player
        '''
