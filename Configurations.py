from sys import platform
import json



class Configurations :
    
    def __init__(self) :
        self.config = json.load("config.json")
        self.media_player = self.config["media_player"]
        self.platform = platform
        self.driver_name = "chromedriver.exe" if platform == "win32" else "chromedriver"
        self.driver_path = f"drivers/{self.driver_name}"
        
        
        