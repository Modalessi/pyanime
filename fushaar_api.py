import requests
import re
from bs4 import BeautifulSoup
from bs4 import element
from selenium_handler import SeleniumHandler

from website_api_interface import WebsiteAPIInterface


class FushaarAPI(WebsiteAPIInterface) :

    WEBSITE_NAME = "Fushaar"
    HTML_PARSER = "html.parser"
    BASE_URL = "https://fushaar.info"



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
        params = {"s" : query}
        result_page = requests.get(FushaarAPI.BASE_URL, params=params, timeout=1000)
        soup = BeautifulSoup(result_page.content, FushaarAPI.HTML_PARSER)

        container_div = soup.find("div", {"id" : "container"})

        results = []

        movies = container_div.find_all("article", {"class" : "poster"})
        results = []

        for movie in movies :
            title = movie.find("div", {"class" : "info"}).h3.text
            link = movie.find("a")["href"]
            isMembersOnly = movie.find("div", {"class" : "box-office"})
            if not isMembersOnly :
                results.append({   
                    "title" : title,
                    "link" : link
                })
        
        return results


        

    @staticmethod
    def is_movie(link: str) -> bool:
        '''
        return wether the webpage link is a movie or not
        this website is for movies only
        '''
        return True


    @staticmethod
    def contains_seasons(link: str) -> bool:
        '''
        return wether the webpage contains seasons or not
        this website is for movies only
        '''
        return False

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
        this website is for movies only
        '''
        return []

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
        this website is for movies only
        '''
        return []

    @staticmethod
    def get_m3u8_link(link: dict) -> str:
        '''
        should return m3u8 link for an episode or a movie
        in order to pass to a media player

        this website provides multiple servers for streaming.
        for now we will use "cloud" server only
        '''

        result_page = requests.get(link, timeout=1000)
        soup = BeautifulSoup(result_page.content, FushaarAPI.HTML_PARSER)
        stream_link = soup.find("a", {"class": "report-bug"})
        stream_link = stream_link["href"]

        return stream_link


