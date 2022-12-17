import time
from bs4 import BeautifulSoup
import requests
from selenium_handler import SeleniumHandler
from website_api_interface import WebsiteAPIInterface


class EgybestAPI(WebsiteAPIInterface):
    WEBSITE_NAME = "Egybest"
    BASE_URL = "https://aero.egybest.mba"
    HTML_PARSER = "html.parser"

    @staticmethod
    def search(query):
        search_url = EgybestAPI.BASE_URL + "/explore/"
        result_page = requests.get(
            search_url, params={"q": query}, timeout=1000)

        soup = BeautifulSoup(result_page.content, EgybestAPI.HTML_PARSER)

        results_divs = soup.find(
            "div", id="movies").findAll("a", class_="movie")

        results = []

        for result_div in results_divs:
            result = {}

            result["link"] = EgybestAPI.BASE_URL + result_div["href"]
            result["title"] = result_div.find("span", class_="title").text

            results.append(result)

        return results

    @staticmethod
    def is_movie(link):
        return not EgybestAPI.contains_seasons(link)

    @staticmethod
    def contains_seasons(link):
        result_page = requests.get(link, timeout=1000)

        soup = BeautifulSoup(result_page.content, EgybestAPI.HTML_PARSER)

        mboxes = soup.find_all("div", class_="mbox")

        for mbox in mboxes:
            strong_tag = mbox.find("strong")
            if strong_tag is not None:
                if "مواسم" in strong_tag.text:
                    return True

        return False

    @staticmethod
    def get_seasons(link):
        result_page = requests.get(link, timeout=1000)

        soup = BeautifulSoup(result_page.content, EgybestAPI.HTML_PARSER)

        mboxes = soup.find("div", id="mainLoad").find_all("div", class_="mbox")

        for mbox in mboxes:
            strong_tag = mbox.find("strong")
            if strong_tag is not None:
                if "مواسم" in strong_tag.text:
                    mboxes = mbox
                    break

        seasons_tags = mboxes.find(
            "div", class_="contents movies_small").find_all("a")

        seasons = []

        index = 0
        for season_tag in seasons_tags:
            season = {}

            season["link"] = EgybestAPI.BASE_URL + season_tag["href"]
            season["title"] = season_tag.find("span", class_="title").text
            season["index"] = index
            index += 1
            seasons.append(season)

        return seasons[::-1]

    @staticmethod
    def get_episodes(link):
        result_page = requests.get(link, timeout=1000)

        soup = BeautifulSoup(result_page.content, EgybestAPI.HTML_PARSER)

        mboxes = soup.find("div", id="mainLoad").find_all("div", class_="mbox")

        for mbox in mboxes:
            strong_tag = mbox.find("strong")
            if strong_tag is not None:
                if "حلقات" in strong_tag.text:
                    mboxes = mbox
                    break

        episode_tags = mboxes.find("div", class_="movies_small") if mboxes.find(
            "div", class_="contents movies_small") is None else mboxes.find("div", class_="contents movies_small")
        episode_tags = episode_tags.find_all("a")

        episodes = []

        index = 0
        for episode_tag in episode_tags:
            episode = {}

            episode["link"] = EgybestAPI.BASE_URL + episode_tag["href"]
            episode["title"] = episode_tag.find("span", class_="title").text
            episode["index"] = index
            index += 1

            episodes.append(episode)

        return episodes[::-1]

    @staticmethod
    def get_m3u8_link(link):
        result_page = requests.get(link, timeout=1000)

        soup = BeautifulSoup(result_page.content, EgybestAPI.HTML_PARSER)

        frame_link = EgybestAPI.BASE_URL + \
            soup.find("iframe", class_="auto-size")["src"]

        driver = SeleniumHandler().driver
        driver.get(frame_link)

        driver.find_element_by_xpath('/html/body/div/i').click()

        page_loaded = False
        while not page_loaded:
            try:
                soup = BeautifulSoup(driver.page_source,
                                     EgybestAPI.HTML_PARSER)
                source = soup.find("video", id="video_html5_api").find(
                    "source")["src"]
                page_loaded = True
            except AttributeError:
                time.sleep(0.75)
                continue

        source = EgybestAPI.BASE_URL + source

        m3u8_file = requests.get(source, timeout=1000)
        m3u8_file = m3u8_file.text.split("\n")

        m3u8_file = list(filter(lambda x: x != "", m3u8_file))
        return m3u8_file[-1]
