import os
from sys import platform
import yaml
from terminal_colors import TerminalColors as tcolors
from terminal_colors import color_print


class Configurations:

    def __init__(self, config_file_path: str = os.path.expanduser("~") + "/.config/pyanime/config.yaml"):
        try:
            with open(config_file_path, "r", encoding="utf-8") as config_file:
                self.config = yaml.load(config_file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            color_print(
                "[!] - Config file not found, creating new one.", tcolors.WARNING)
            self.config = self._create_config_file()
            print("\n\n")

    def _create_config_file(self):
        config = {}

        config["platform"] = platform
        config["media_player"] = "mpv"
        config["preferred_quility"] = "best"
        config["driver_path"] = "global"

        # create new directory in .config
        try:
            os.mkdir(os.path.expanduser("~") + "/.config/pyanime")
        except FileExistsError:
            pass

        # create config file
        config_file_path = os.path.expanduser(
            "~") + "/.config/pyanime/config.yaml"
        config_file = open(config_file_path, "w", encoding="utf-8")
        yaml.dump(config, config_file)
        config_file.close()

        return config
