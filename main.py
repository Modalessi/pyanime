import os
import sys

from entry import Entry, EntryState
from egybest_api import EgybestAPI
from faselhd_api import FaselhdAPI
from witanime_api import WitAnimeAPI
from terminal_colors import TerminalColors as tcolors 
from terminal_colors import color_input, color_print
from configurations import Configurations

configs = Configurations().config


def input_is_valid(num, minimum: int, maximum: int):
    """
    Checks if input in valid.
    input is valid if it is in range [mn, mx]
    """

    if num.isdigit():
        num = int(num)
        if num < minimum or num > maximum:
            return False
    else:
        return False

    return True


def show_table(elements: list, color1: str, color2: str):
    """
    prints elements in list format.
    """

    if len(elements) == 0:
        color_print("[*] No Result", tcolors.FAIL)
        return

    for index, element in enumerate(elements):
        if index % 2 == 0:
            color_print(f"[{index + 1}] {element}", color1)
        else:
            color_print(f"[{index + 1}] {element}", color2)


def ask_for_search_query() -> list:
    search_query = color_input("[*] - Enter search query : ", tcolors.OKGREEN)
    faselhd_results = FaselhdAPI.search(search_query)
    # witanime_results = WitAnimeAPI.search(search_query)
    # egybest_results = EgybestAPI.search(search_query)

    results = []

    for result in faselhd_results: # + egybest_results:
        if result in faselhd_results:
            result["source"] = FaselhdAPI
            result["title"] = f'[{result["source"].WEBSITE_NAME}] {result["title"]}'
        else:
            result["source"] = EgybestAPI
            result["title"] = f'[{result["source"].WEBSITE_NAME}] {result["title"]}'

        results.append(result)

    return results


def ask_for_selection(results: list) -> dict:
    show_table([result["title"]
               for result in results], tcolors.OKBLUE, tcolors.OKCYAN)
    enterd_choice = color_input("[*] - Enter choice: ", tcolors.OKGREEN)

    if not input_is_valid(enterd_choice, 1, len(results)):
        color_print("[-] - Invalid choice.", tcolors.FAIL)
        raise Exception("Invalid choice")

    selected_result = results[int(enterd_choice) - 1]
    return selected_result


def show_player_options(curr_ep: int, total_eps: int):
    player_options = "\n\n"
    player_options += tcolors.OKGREEN + \
        "[n] - Next Episode" + tcolors.ENDC if curr_ep < total_eps else ""
    player_options += tcolors.OKBLUE + \
        "\n[p] - Previous Episode" + tcolors.ENDC if curr_ep > 1 else ""
    player_options += tcolors.OKCYAN + \
        "\n[e] - Select Episode" + tcolors.ENDC if total_eps > 1 else ""
    player_options += tcolors.OKCYAN + "\n[s] - Search" + tcolors.ENDC
    player_options += tcolors.OKCYAN + "\n[q] - quit" + tcolors.ENDC

    player_options += tcolors.OKCYAN + "\n\nEnter option: " + tcolors.ENDC
    return color_input(player_options, tcolors.OKCYAN)


def main():
<<<<<<< HEAD
    os.system("")
        
    search_query = color_input("[*] - Enter search query: ", tcolors.OKGREEN)
    faselhd_results = FaselhdAPI.search(search_query)
    egybest_results = EgybestAPI.search(search_query)
    
    results = []
    
    for i ,result in enumerate(faselhd_results + egybest_results) :
        if result in faselhd_results :
            result["source"] = "faselhd"
        else :
            result["source"] = "egybest"
            
        color_print(f"{i + 1} - [{result['source']}] {result['title']}", tcolors.OKBLUE if result["source"] == "faselhd" else tcolors.OKCYAN)
        
        results.append(result)
    
    
    if len(results) == 0 :
        color_print("[-] - No results found.", tcolors.FAIL)
        return
    
    
    enterd_choice = color_input("[*] - Enter choice: ", tcolors.OKGREEN)
    
    if not input_is_valid(enterd_choice, 1, len(results)):
        color_print("[-] - Invalid choice.", tcolors.FAIL)
        return
    
    selected_result = results[int(enterd_choice) - 1]
    
    if selected_result["source"] == "faselhd":
        
        if FaselhdAPI.is_movie(selected_result) :
            m3u8_link = FaselhdAPI.get_m3u8_link(selected_result)
            present_player_with_episode(m3u8_link)
            return
        
        if FaselhdAPI.contains_seasons(selected_result) :
            seasons = FaselhdAPI.get_seasons(selected_result)
            show_table([season["title"] for season in seasons], tcolors.OKBLUE, tcolors.OKCYAN)
            
            enterd_season = color_input("[*] - Enter season: ", tcolors.OKGREEN)
            
            if not input_is_valid(enterd_season, 1, len(seasons)):
                color_print("[-] - Invalid season.", tcolors.FAIL)
                return
            
            selected_result = seasons[int(enterd_season) - 1]
        
        episodes = FaselhdAPI.get_episodes(selected_result)
        show_table([episode["title"] for episode in episodes], tcolors.OKBLUE, tcolors.OKCYAN)
        
        enterd_episode = color_input("[*] - Enter episode: ", tcolors.OKGREEN)
        
        if not input_is_valid(enterd_episode, 1, len(episodes)):
            color_print("[-] - Invalid episode.", tcolors.FAIL)
            return
        
        selected_result = episodes[int(enterd_episode) - 1]
        
        m3u8_link = FaselhdAPI.get_m3u8_link(selected_result)
        if "-qr" in sys.argv :
            generateQRCode(m3u8_link)
        else :
            present_player_with_episode(m3u8_link)
        
    
    
            
        
    elif selected_result["source"] == "egybest" :
        if EgybestAPI.is_movie(selected_result) :
            m3u8_link = EgybestAPI.get_m3u8_link(selected_result)
            present_player_with_episode(m3u8_link)
            return
        
        if EgybestAPI.contains_seasons(selected_result) :
            seasons = EgybestAPI.get_seasons(selected_result)
            show_table([season["title"] for season in seasons], tcolors.OKBLUE, tcolors.OKCYAN)
            
            enterd_season = color_input("[*] - Enter season: ", tcolors.OKGREEN)
            
            if not input_is_valid(enterd_season, 1, len(seasons)):
                color_print("[-] - Invalid season.", tcolors.FAIL)
                return
            
            selected_result = seasons[int(enterd_season) - 1]
        
        episodes = EgybestAPI.get_episodes(selected_result)
        show_table([episode["title"] for episode in episodes], tcolors.OKBLUE, tcolors.OKCYAN)
        
        enterd_episode = color_input("[*] - Enter episode: ", tcolors.OKGREEN)
        
        if not input_is_valid(enterd_episode, 1, len(episodes)):
            color_print("[-] - Invalid episode.", tcolors.FAIL)
            return
        
        selected_result = episodes[int(enterd_episode) - 1]
        
        m3u8_link = EgybestAPI.get_m3u8_link(selected_result)
        if "-qr" in sys.argv :
            generateQRCode(m3u8_link)
        else :
            present_player_with_episode(m3u8_link)
        
    
        
        
    
    
    
    
=======

    # show colors in windows cmd
    os.system("")

    entry = Entry()

    exit_app = False
    option = ""
    while not exit_app:
        if entry.state == EntryState.ASK_FOR_QUERY:
            search_results = ask_for_search_query()
            selected_result = ask_for_selection(search_results)
            entry.set_query_selected(
                selected_result["title"], selected_result["link"], selected_result["source"])

        if entry.state == EntryState.QUERY_SELECTED:
            if entry.is_movie:
                entry.get_m3u8_link()
                entry.set_playing()

            if entry.contains_seasons:
                seasons = entry.get_seasons()
                selected_season = ask_for_selection(seasons)
                entry.set_season_selected(selected_season)

        if entry.state in [EntryState.SEASON_SELECTED, EntryState.QUERY_SELECTED]:
            episodes = entry.get_episodes()
            selected_episode = ask_for_selection(episodes)
            entry.set_episode_selected(selected_episode)

            entry.get_m3u8_link()
            entry.set_playing()

        if entry.state == EntryState.PLAYING:
            if entry.is_movie:
                option = show_player_options(1, 1)
            else:
                option = show_player_options(
                    entry.selected_episode["index"] + 1, len(entry.episodes))

        if option.lower() == "n":
            entry.next_episode()
        elif option.lower() == "p":
            entry.previous_episode()
        elif option.lower() == "e":
            entry.revers_state()
        elif option.lower() == "s":
            entry = Entry()
        elif option.lower() == "q":
            exit_app = True


>>>>>>> refactoring
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        color_print("\n[*] - exiting...", tcolors.WARNING)
        sys.exit(0)
