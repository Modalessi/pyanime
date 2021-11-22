from selenium import webdriver
import selenium
import json
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib.parse
from bs4 import BeautifulSoup
import requests
from terminalColors import *
import os


HTML_PARSER = "html.parser"
BASE_URL = "https://www.faselhd.pro/"

CLI_COMMAND = "unbuffer -p /usr/local/bin/iina-cli '<M3U8 Link>'"

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# /Applications/Google Chrome.app/Contents/MacOS/Google Chrome

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




def get_anime_episodes(search_result) :
	
	titile = search_result["title"]
	link = search_result["link"]
	
	reqult_page = requests.get(link)
	soup = BeautifulSoup(reqult_page.content, HTML_PARSER)
	
	episodes = {}
	
	episodes_div = soup.find("div", id = "epAll")
	links = episodes_div.find_all("a")
	
	for link in links:
		episodes[link.text.strip()] = link["href"]
	
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
	
	# print("frame_link = ", frame_link)
	driver.get(frame_link)
	frame_soup = BeautifulSoup(driver.page_source, HTML_PARSER)
	
	# print(frame_soup.prettify())
	
	buttons_div = frame_soup.find("div", class_="quality_change")
	quilities_buttons = buttons_div.find_all("button", class_="hd_btn")
	# print("quilities_buttons = ", quilities_buttons)
	quilities = [int(btn["data-quality"]) if btn["data-quality"] != "auto" else 0 for btn in quilities_buttons]
	# print("quilities = ", quilities)
	highest_quality = max(quilities)
	
	# get button where text is highest quality
	button = driver.find_element_by_xpath(f"//button[@data-quality='{highest_quality}']")
	# try :
	# 	button.click()
	# except selenium.common.exceptions.ElementClickInterceptedException :
	# 	print("ElementClickInterceptedException: clicking again after 5 sec")
	# 	button.click()
	
	driver.execute_script("$('.hd_btn').click();")
	time.sleep(0.5)
	
	while True:
		browser_log = driver.get_log('performance') 
		events = [process_browser_log_entry(entry) for entry in browser_log]
		events = [event for event in events if 'Network.response' in event['method']]
		for event in events:
			# print("evern  = ", json.dumps(event))
			try : 
				url = event['params']['response']['url']
			except KeyError :
				continue
			if "https://co8bau0l.faselhdstream.com/stream" in url :
				# driver.quit()
				# print("="*100, "fount the url", "\n", url)
				return event['params']['response']['url']
	
	

	
	

def main() :
	search_query = color_input("[ * ] - Enter search query: ", tcolors.OKGREEN)
	results = search(search_query)
	
	for index, anime in enumerate(results):
		color_print("[ " + str(index + 1) + " ] : " + anime["title"], tcolors.OKCYAN)
	
	result_number = color_input("[ * ] - Enter number: ", tcolors.OKGREEN)
	
	if result_number.isdigit():
		result_number = int(result_number) - 1
		if result_number < 0 or result_number >= len(results):
			color_print("[ * ] - Invalid number", tcolors.FAIL)
			return
	else :
		color_print("[ ERROR ] - Invalid number", tcolors.FAIL)
		return
	
	anime = results[result_number]
	episodes = get_anime_episodes(anime)
	
	for index, (episode, link) in enumerate(episodes.items()):
		color_print(f"[ {index + 1} ] - {episode} ", tcolors.OKCYAN)
	
	episode_number = color_input("[ * ] - Enter episode number: ", tcolors.OKGREEN)
	
	if episode_number.isdigit():
		episode_number = int(episode_number) - 1
		if episode_number < 0 or episode_number >= len(episodes):
			color_print("[ * ] - Invalid number", tcolors.FAIL)
			return
	else :
		color_print("[ ERROR ] - Invalid number", tcolors.FAIL)
		return
	
	selected_episode = episodes[list(episodes.keys())[episode_number]]
	m3u8_link = get_m3u8_link(selected_episode)
	
	command = CLI_COMMAND.replace("<M3U8 Link>", m3u8_link)
	os.system(command)
	
	
	
	
	
	
	
	
main()