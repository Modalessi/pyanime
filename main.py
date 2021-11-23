from typing import Collection
from requests.api import get
from selenium import webdriver
import selenium
import json
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib.parse
from bs4 import BeautifulSoup, element
import requests
from terminalColors import *
import os


HTML_PARSER = "lxml"
BASE_URL = "https://www.faselhd.pro/"
PLAYER = "iina"
	
	
def input_is_valid(n, mn, mx) :
	if n.isdigit():
		if n < mn or n > mx:
			return False
	else :
		return False
	
	return True

	

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome("bin/chromedriver", options=options, desired_capabilities=caps)


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

def search(query):
    search_url = BASE_URL + "?s=" + urllib.parse.quote_plus(query)
    reqult_page = requests.get(search_url)
    soup = BeautifulSoup(reqult_page.content, HTML_PARSER)
    
    animes_div = soup.find("div", id="postList")
    animes = animes_div.find_all("div", class_="col-xl-2 col-lg-2 col-md-3 col-sm-3")
    
    results = []
    
    for anime_div in animes:
        post_div = anime_div.find("div", class_="postDiv").find("a")
        anime = {}
        
        anime["link"] = post_div["href"]
        anime["title"] = post_div.find("div", class_ = "postInner").find("div", class_ = "h1").text
        
        results.append(anime)
    
    return results



def get_seasons(search_result):
	title = search_result["title"]
	link = search_result["link"]
	
	reqult_page = requests.get(link)
	soup = BeautifulSoup(reqult_page.content, HTML_PARSER)
	
	
	seasons = []
	seasons_div = soup.find("div", id = "seasonList")
	seasons_divs = seasons_div.find_all("div", class_="col-xl-2 col-lg-3 col-md-6")
	
	for season_div in seasons_divs:
		base_url = "https://www.faselhd.pro/?p="
		season = {}
		
		season_id = seasons_div.find("div", class_="seasonDiv")["data-href"]
		season["link"] = base_url + season_id
		season["title"] = season_div.find("div", class_="seasonDiv").find("div", class_="title").text
		
		seasons.append(season)
	return seasons
	

def get_anime_episodes(search_result) :
	
	title = search_result["title"]
	link = search_result["link"]
	
	reqult_page = requests.get(link)
	soup = BeautifulSoup(reqult_page.content, HTML_PARSER)
	
	episodes = {}
		
	episodes_div = soup.find("div", id = "epAll")
	links = episodes_div.find_all("a")
	
	for link in links:
		episode = {}
		episode["link"] = link["href"]
		episode["title"] = link.text.strip()
		episodes.append(episode)
	
	return episodes




def get_m3u8_link(episode_link):
	
	reqult_page = requests.get(episode_link)
	soup = BeautifulSoup(reqult_page.content, HTML_PARSER)
	frames = soup.find_all("iframe")
	
	frame_link = ""
	for frame in frames:
		if frame["name"] == "player_iframe" :
			frame_link = frame["src"]
			break
	
	driver.get(frame_link)
	frame_soup = BeautifulSoup(driver.page_source, HTML_PARSER)
	
	
	buttons_div = frame_soup.find("div", class_="quality_change")
	quilities_buttons = buttons_div.find_all("button", class_="hd_btn")
	quilities = [int(btn["data-quality"]) if btn["data-quality"] != "auto" else 0 for btn in quilities_buttons]
	highest_quality = max(quilities)
	
	
	driver.execute_script("$('.hd_btn').click();")
	time.sleep(0.5)
	
	while True:
		browser_log = driver.get_log('performance') 
		events = [process_browser_log_entry(entry) for entry in browser_log]
		events = [event for event in events if 'Network.response' in event['method']]
		for event in events:
			try : 
				url = event['params']['response']['url']
			except KeyError :
				continue
			if "faselhdstream.com/stream/hls" in url :
				return event['params']['response']['url']
	
	

def contains_seasons(search_result):
	link = search_result["link"]
	reqult_page = requests.get(link)
	soup = BeautifulSoup(reqult_page.content, HTML_PARSER)
	seasons_div = soup.find("div", id = "seasonList")
	
	return seasons_div != None
	


def show_table(elements, color1, color2) :
	for index, element in enumerate(elements):
		if index % 2 == 0 :
			color_print(f"[{index + 1}] {element}", color1)
		else :
			color_print(f"[{index + 1} {element}", color2)
	


def controller(episodes, currentIndex) :
	
	present_player_with_episode(episodes[currentIndex - 1])
	color_print(f"Currently playing [{currentIndex} / {len(episodes)}]", tcolors.OKGREEN)

	if currentIndex < len(episodes) :
		color_print(f"	[n] to play next episode", tcolors.OKCYAN)
	
	if currentIndex > 1 :
		color_print(f"	[p] to play previous episode", tcolors.OKBLUE)
	
	
	color_print(f"	[q] to exit", tcolors.WARNING)
	
	choice = color_input(f"	[*] choice: ", tcolors.OKGREEN)
	
	if choice.lower() == "n" :
		controller(episodes, currentIndex + 1)
	elif choice.lower() == "p" :
		controller(episodes, currentIndex - 1)
	elif choice.lower() == "q" :
		return
	else :
		color_print("Invalid input", tcolors.FAIL)
		return


def present_player_with_episode(episode) :
	m3u8_link = get_m3u8_link(episode["link"])
	
	if PLAYER == "iina" :
		cli_command = "unbuffer -p /usr/local/bin/iina-cli " + m3u8_link
		os.system(cli_command)
	


def main() :
	search_query = color_input("[ * ] - Enter search query: ", tcolors.OKGREEN)
	results = search(search_query)
	
	show_table([result["title"] for result in results], tcolors.OKCYAN, tcolors.OKBLUE)
	
	enterd_choice = color_input("[ * ] - Enter number: ", tcolors.OKGREEN)
	
	if not input_is_valid(enterd_choice, 1, len(results)) :
		color_print(f"[ ERROR] invalid input")
		return
	
	choosen_result = results[enterd_choice - 1]
	
	if contains_seasons(choosen_result) :
		seasons = get_seasons(choosen_result)
		show_table([season["title"] for season in seasons], tcolors.OKCYAN, tcolors.OKBLUE)
		
		enterd_choice = color_input("[ * ] - Enter number: ", tcolors.OKGREEN)
		if not input_is_valid(enterd_choice, 1, len(seasons)) :
			color_print(f"[ ERROR] invalid input", tcolors.FAIL)
			return
		
		season = seasons[enterd_choice - 1]
		episodes = get_anime_episodes(season)
	else :
		episodes = get_anime_episodes(choosen_result)
	
	
	show_table([episode["title"] for episode in episodes])
	
	episode_number = color_input("[ * ] - Enter episode number: ", tcolors.OKGREEN)
	enterd_choice = color_input("[ * ] - Enter number: ", tcolors.OKGREEN)
	
	if not input_is_valid(enterd_choice, 1, len(episodes)) :
		color_print(f"[ ERROR] invalid input", tcolors.FAIL)
		return
	
	
	controller(episodes, enterd_choice)
	
	
	
	
	

main()