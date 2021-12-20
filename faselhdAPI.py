from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import requests
import sys



class FaselhdAPI() :
    
    HTML_PARSER = "html.parser"
    BASE_URL = BASE_URL = "https://www.faselhd.pro/"
    
    # Takes a query to search in fasel hd website and returns a list of dictionaries
    def search(query):
        
        reqult_page = requests.get(FaselhdAPI.BASE_URL, params = {"s": query})
        soup = BeautifulSoup(reqult_page.content, FaselhdAPI.HTML_PARSER)

        animes_div = soup.find("div", id="postList")
        animes = animes_div.find_all("div", class_="col-xl-2 col-lg-2 col-md-3 col-sm-3")

        results = []

        for anime_div in animes:
            post_div = anime_div.find("div", class_="postDiv").find("a")
            result = {}

            result["link"] = post_div["href"]
            result["title"] = post_div.find("div", class_="postInner").find("div", class_="h1").text

            results.append(result)

        return results
        
    
    # takes a search result and returns if it is a movie or not
    def is_movie(result) :
        link = result["link"]

        reqult_page = requests.get(link)
        soup = BeautifulSoup(reqult_page.content, FaselhdAPI.HTML_PARSER)

        episodes_div = soup.find("div", id="epAll")

        return episodes_div == None
        
        
    # takes a search result and returnn a it have seasons or not
    def contains_seasons(result) :
        link = result["link"]
        reqult_page = requests.get(link)
        soup = BeautifulSoup(reqult_page.content, FaselhdAPI.HTML_PARSER)
        seasons_div = soup.find("div", id="seasonList")

        return seasons_div != None
        
        
    # takes a search result and returns a list of dictionaries with the seasons
    # each season can be treated as a search result
    def get_seasons(result) :
        link = search_result["link"]

        reqult_page = requests.get(link)
        soup = BeautifulSoup(reqult_page.content, FaselhdAPI.HTML_PARSER)

        seasons = []
        seasons_div = soup.find("div", id="seasonList")
        seasons_divs = seasons_div.find_all("div", class_="col-xl-2 col-lg-3 col-md-6")

        for season_div in seasons_divs:
            base_url = "https://www.faselhd.pro/?p="
            season = {}

            season_id = seasons_div.find("div", class_="seasonDiv")["data-href"]
            season["link"] = base_url + season_id
            season["title"] = season_div.find("div", class_="seasonDiv").find("div", class_="title").text

            seasons.append(season)
        return seasons
        
    
    # takes a search result and returns a list of dictionaries with the episodes
    # each episode can be treated as a search result
    def get_episodes(result) :            
        link = result["link"]

        reqult_page = requests.get(link)
        soup = BeautifulSoup(reqult_page.content, FaselhdAPI.HTML_PARSER)

        episodes = []

        episodes_div = soup.find("div", id="epAll")
        links = episodes_div.find_all("a")

        for link in links:
            episode = {}
            episode["link"] = link["href"]
            episode["title"] = link.text.strip()
            episodes.append(episode)

        return episodes
        
    
    
    # this is the worst function i wrote 
    # i beleive there can be a better way to do this
    # however in order to make this work i had to use selenium
    # this method takes an episode link or a movie link and returns m3u8 link
    # m3u8 link can then be passed to media player to play the video
    def get_m3u8_link(result):
        
        reqult_page = requests.get(result["link"])
        soup = BeautifulSoup(reqult_page.content, FaselhdAPI.HTML_PARSER)
        frames = soup.find_all("iframe")

        frame_link = ""
        for frame in frames:
            if frame["name"] == "player_iframe":
                frame_link = frame["src"]
                break
            
            
        driver_name = "chromedriver.exe" if sys.platform == "win32" else "chromedriver"
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        service = Service(f"drivers/{driver_name}")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=service, options=options, desired_capabilities=caps)
        driver.get(frame_link)

        driver.execute_script("$('.hd_btn').click();")
        time.sleep(0.5)
        
        
        while True:
            browser_log = driver.get_log('performance')
            events = [(json.loads(entry['message'])['message']) for entry in browser_log]
            events = [event for event in events if 'Network.response' in event['method']]
            for event in events:
                try:
                    url = event['params']['response']['url']
                except KeyError:
                    continue
                if "faselhdstream.com/stream/hls" in url:
                    return event['params']['response']['url']
                    
                    
        
        
        
        
        
            
            
        
        
            
