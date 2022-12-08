import os
import sys

from Entry import Entry
from EntryState import EntryState
from egybestAPI import EgybestAPI
from faselhdAPI import FaselhdAPI
from terminalColors import *
from Configurations import Configurations
from WebsiteAPIInterface import WebsiteAPIInterface

configs = Configurations().config


def input_is_valid(n, mn: int, mx: int):
    """
    Checks if input in valid.
    input is valid if it is in range [mn, mx]
    """
    
    if n.isdigit():
        n = int(n)
        if n < mn or n > mx:
            return False
    else:
        return True if n.lowercase() == "b" else False

    return True


def present_player_with_episode(m3u8_link: str):
    """
    starts player with m3u8 link
    """ 
    media_player = configs["media_player"]
    if media_player == "iina-cli":
        cli_command = f"unbuffer -p {media_player} '{m3u8_link}'"
        os.system(cli_command)
    else:
        cli_command = f"{media_player} --no-terminal \"{m3u8_link}\""
        os.system(cli_command)


def show_table(elements: list, color1: str, color2: str):
    """
    prints elements in list format.
    """

    if len(elements) == 0 :
        color_print("[*] No Result", tcolors.FAIL)
        return
    

    for index, element in enumerate(elements):
        if index % 2 == 0:
            color_print(f"[{index + 1}] {element}", color1)
        else:
            color_print(f"[{index + 1}] {element}", color2)

    


def ask_for_search_query()-> list :
    search_query = color_input("[*] - Enter search query : ", tcolors.OKGREEN)
    faselhd_results = FaselhdAPI.search(search_query)
    egybest_results = EgybestAPI.search(search_query)
    
    results = []
    
    for result in faselhd_results + egybest_results :
        if result in faselhd_results :
            result["source"] = FaselhdAPI
            result["title"] = f'[{result["source"].WEBSITE_NAME}] {result["title"]}'
        else :
            result["source"] = EgybestAPI
            result["title"] = f'[{result["source"].WEBSITE_NAME}] {result["title"]}'
                    
        results.append(result)
    
    return results


def ask_for_selection(results: list)-> dict :
    show_table([result["title"] for result in results], tcolors.OKBLUE, tcolors.OKCYAN)
    enterd_choice = color_input("[*] - Enter choice (b to go back): ", tcolors.OKGREEN)
    
    if not input_is_valid(enterd_choice, 1, len(results)):
        color_print("[-] - Invalid choice.", tcolors.FAIL)
        # TODO: Make Custom Exception and throw it
    
    return None if enterd_choice.lower() == "b" else results[int(enterd_choice) - 1]


def main():
    
    # show colors in windows cmd
    os.system("")
    
    entry = Entry()

    exit = False

    search_results = ask_for_search_query()
    selected_result = ask_for_selection(search_results)
    entry.set_query_selected(selected_result["title"], selected_result["link"], selected_result["source"])
    

    if entry.is_movie :
        m3u8_link = entry.get_m3u8_link()
        present_player_with_episode(m3u8_link)
        return
    
    if entry.contains_seasons :
        seasons = entry.get_seasons()
        selected_season = ask_for_selection(seasons)
        entry.set_season_selected(selected_season)
    
    episodes = entry.get_episodes()
    selected_episode = ask_for_selection(episodes)
    entry.set_episode_selected(selected_episode)
    
    m3u8_link = entry.get_m3u8_link()
    present_player_with_episode(m3u8_link)
        
    
        

    
if __name__ == "__main__":
    try :
        main()
    except KeyboardInterrupt:
        color_print("\n[*] - Exiting...", tcolors.WARNING)
        sys.exit(0)