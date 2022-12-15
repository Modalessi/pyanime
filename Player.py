import subprocess as sp
from configurations import Configurations


def start_player(entry):

    if entry.selected_episode:
        media_title = entry.title + " - " + entry.selected_episode["title"]
    elif entry.is_movie:
        media_title = entry.title
    else:
        raise Exception("entry is not a movie or an episode")

    if Configurations().config["media_player"] in ["mpv", "iina"]:
        player_command = [
            f"{Configurations().config['media_player']}",
            f"{entry.m3u8_link}",
            f"--force-media-title={media_title}"
        ]
    else:
        raise Exception("media player not supported")

    subprocess = sp.Popen(player_command, stdout=sp.PIPE, stderr=sp.DEVNULL)
    return subprocess
