import json
import sys
from egybestAPI import EgybestAPI
from faselhdAPI import FaselhdAPI
from terminalColors import *
import os



CONFIG_FILE = "config.json"

with open(CONFIG_FILE) as f:
    configurations = json.load(f)


def input_is_valid(n: int, mn: int, mx: int):
    """
    Checks if input in valid.
    input is valid if it is in range [mn, mx]
    """
    
    if n.isdigit():
        n = int(n)
        if n < mn or n > mx:
            return False
    else:
        return False

    return True




def present_player_with_episode(m3u8_link: str):
    """
    starts player with m3u8 link
    """
    
    player = configurations["media_player"]
    if player == "iina-cli":
        cli_command = f"unbuffer -p {player} '{m3u8_link}'"
        os.system(cli_command)
    else:
        cli_command = f"{player} --no-terminal \"{m3u8_link}\""
        os.system(cli_command)


def show_table(elements: list, color1: str, color2: str):
    """
    prints elements in list format.
    """
    for index, element in enumerate(elements):
        if index % 2 == 0:
            color_print(f"[{index + 1}] {element}", color1)
        else:
            color_print(f"[{index + 1}] {element}", color2)

    


def main():
        
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
        present_player_with_episode(m3u8_link)
        
    
        
        
    
    
    
    
if __name__ == "__main__":
    try :
        main()        
    except KeyboardInterrupt:
        color_print("\n[*] - Exiting...", tcolors.WARNING)
        sys.exit(0)