import json
from faselhdAPI import FaselhdAPI
from terminalColors import *
import os



HTML_PARSER = "html.parser"
BASE_URL = "https://www.faselhd.pro/"

CONFIG_FILE = "config.json"

with open(CONFIG_FILE) as f:
    configurations = json.load(f)


def input_is_valid(n, mn, mx):
    if n.isdigit():
        n = int(n)
        if n < mn or n > mx:
            return False
    else:
        return False

    return True


def present_player_with_episode(m3u8_link):

    player = configurations["media_player"]

    if player == "iina":
        cli_command = f"unbuffer -p {player} '{m3u8_link}'"
        os.system(cli_command)
    else:
        cli_command = f"{player} --no-terminal '{m3u8_link}'"
        os.system(cli_command)


def show_table(elements, color1, color2):
    for index, element in enumerate(elements):
        if index % 2 == 0:
            color_print(f"[{index + 1}] {element}", color1)
        else:
            color_print(f"[{index + 1}] {element}", color2)



def main():
    
    search_query = color_input("[*] - Enter search query: ", tcolors.OKGREEN)
    faselhd_results = FaselhdAPI.search(search_query)

    if len(faselhd_results) == 0:
        color_print("[!] - No results found :(", tcolors.FAIL)
        return

    show_table([result["title"] for result in faselhd_results], tcolors.OKCYAN, tcolors.OKBLUE)

    enterd_choice = color_input("[*] - Enter number: ", tcolors.OKGREEN)

    if not input_is_valid(enterd_choice, 1, len(faselhd_results)):
        color_print(f"[ERROR] invalid input", tcolors.FAIL)
        return

    choosen_result = faselhd_results[int(enterd_choice) - 1]

    if FaselhdAPI.is_movie(choosen_result):
        color_print("Enjoy ;)", tcolors.OKBLUE)
        present_player_with_episode(choosen_result)
        return

    if FaselhdAPI.contains_seasons(choosen_result):
        seasons = FaselhdAPI.get_seasons(choosen_result)
        show_table([season["title"] for season in seasons], tcolors.OKCYAN, tcolors.OKBLUE)

        enterd_choice = color_input("[ * ] - Enter number: ", tcolors.OKGREEN)
        if not input_is_valid(enterd_choice, 1, len(seasons)):
            color_print(f"[ERROR] invalid input", tcolors.FAIL)
            return

        season = seasons[int(enterd_choice) - 1]
        episodes = FaselhdAPI.get_episodes(season)
    else:
        episodes = FaselhdAPI.get_episodes(choosen_result)

    show_table([episode["title"] for episode in episodes], tcolors.OKBLUE, tcolors.OKCYAN)

    enterd_choice = color_input("[*] - Enter number: ", tcolors.OKGREEN)

    if not input_is_valid(enterd_choice, 1, len(episodes)):
        color_print(f"[ERROR] invalid input", tcolors.FAIL)
        return

    color_print("Enjoy ;)", tcolors.OKBLUE)
    present_player_with_episode(FaselhdAPI.get_m3u8_link(episodes[int(enterd_choice) - 1]))


main()
