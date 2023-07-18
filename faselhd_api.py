import requests
import re
from bs4 import BeautifulSoup
from selenium_handler import SeleniumHandler
from website_api_interface import WebsiteAPIInterface
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class FaselhdAPI(WebsiteAPIInterface):
    '''
    FaselhdAPI confirms to WebsiteAPIInterface
    it proviedes an interface to search and pull data from faselhd website
    '''

    WEBSITE_NAME = "FaselHD"
    HTML_PARSER = "html.parser"
    BASE_URL = "https://www.faselhd.ac"

    @staticmethod
    def search(query):
        '''
        Takes a query to search in fasel hd website and returns a list of dictionaries
        '''

        result_page = requests.get(FaselhdAPI.BASE_URL, params={
                                   "s": query}, timeout=1000)
        soup = BeautifulSoup(result_page.content, FaselhdAPI.HTML_PARSER)

        animes_div = soup.find("div", id="postList")
        animes = animes_div.find_all(
            "div", class_="col-xl-2 col-lg-2 col-md-3 col-sm-3")

        results = []

        for anime_div in animes:
            post_div = anime_div.find("div", class_="postDiv").find("a")
            result = {}

            result["link"] = post_div["href"]
            result["title"] = post_div.find(
                "div", class_="postInner").find("div", class_="h1").text

            results.append(result)

        return results

    @staticmethod
    def is_movie(link):
        '''
        takes a webpage link and returns if it is a movie or not
        '''

        result_page = requests.get(link, timeout=1000)
        soup = BeautifulSoup(result_page.content, FaselhdAPI.HTML_PARSER)

        episodes_div = soup.find("div", id="epAll")

        return episodes_div is None

    @staticmethod
    def contains_seasons(link):
        '''
        takes a webpage link and returnn a it have seasons or not
        '''
        reqult_page = requests.get(link, timeout=1000)
        soup = BeautifulSoup(reqult_page.content, FaselhdAPI.HTML_PARSER)
        seasons_div = soup.find("div", id="seasonList")

        return seasons_div is not None

    @staticmethod
    def get_seasons(link):
        '''
        takes a webpage link and returns a list of dictionaries with the seasons
        each season can be treated as a search result
        '''

        result_page = requests.get(link, timeout=1000)
        soup = BeautifulSoup(result_page.content, FaselhdAPI.HTML_PARSER)

        seasons = []
        seasons_div = soup.find("div", id="seasonList")
        seasons_divs = seasons_div.find_all(
            "div", class_="col-xl-2 col-lg-3 col-md-6")

        index = 0
        for season_div in seasons_divs:
            base_url =  FaselhdAPI.BASE_URL + "/?p="
            season = {}

            season_id = re.search(r"\?p=(\d+)", season_div.find("div", class_="seasonDiv")["onclick"]).group(1)
            season["link"] = base_url + str(season_id)
            season["title"] = season_div.find(
                "div", class_="seasonDiv").find("div", class_="title").text
            season["index"] = index
            index += 1

            seasons.append(season)
        return seasons

    @staticmethod
    def get_episodes(link):
        '''
        takes a webpage link and returns a list of dictionaries with the episodes
        each episode can be treated as a search result
        '''


        result_page = requests.get(link, timeout=1000)
        soup = BeautifulSoup(result_page.content, FaselhdAPI.HTML_PARSER)

        episodes = []

        episodes_div = soup.find("div", id="epAll")
        links = episodes_div.find_all("a")

        index = 0
        for link in links:
            episode = {}
            episode["link"] = link["href"]
            episode["title"] = link.text.strip()
            episode["index"] = index
            index += 1
            episodes.append(episode)

        return episodes

    @staticmethod
    def get_m3u8_link(link):
        '''
        this method takes an episode or a movie and returns m3u8 link
        m3u8 link can then be passed to media player to play the video
        this is the worst function i have ever wrote
        '''

        try:
            result_page = requests.get(link, timeout=1000)
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None
    
        soup = BeautifulSoup(result_page.content, FaselhdAPI.HTML_PARSER)
        frame = soup.find("iframe", {"name": "player_iframe"})
        if not frame:
            print("Error: player_iframe not found")
            return None

        frame_link = frame["src"]


        driver = SeleniumHandler().driver
        driver.get(frame_link)

        try:
            driver.get(frame_link)

            wait = WebDriverWait(driver, 10)  # wait up to 10 seconds
            # wait until a button with class "hd_btn" is present
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.hd_btn")))

            soup = BeautifulSoup(driver.page_source, FaselhdAPI.HTML_PARSER)
            buttons = soup.find_all("button", class_="hd_btn")
            if buttons:
                buttons.pop(0)
                buttons.sort(key=lambda x: int(x.text[:-1]))
                return buttons[-1]["data-url"]

        except Exception as e:
            print(f"Error: {e}")

        finally:
            driver.close()

        print("Error: Unable to generate m3u8 link")
        return None
