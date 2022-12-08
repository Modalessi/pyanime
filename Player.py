import subprocess as sp
from Configurations import Configurations

def start_player(entry) :

    media_title = entry.title + " - " + entry.selected_episode["title"]

    if Configurations().config["media_player"] in ["mpv", "iina"] :
        player_command = [
            f"{Configurations().config['media_player']}",
            f"{entry.m3u8_link}",
            f"--force-media-title={media_title}"
        ]
    else :
        raise Exception("media player not supported")
    
    subprocess = sp.Popen(player_command, stdout=sp.PIPE, stderr=sp.DEVNULL)    
    return subprocess


        

