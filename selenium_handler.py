import sys
from selenium import webdriver
from selenium import common
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from configurations import Configurations
from terminal_colors import TerminalColors as tcolors
from terminal_colors import color_print


class SeleniumHandler:
    def __init__(self):
        config = Configurations().config
        self.driver_path = None if config["driver_path"] == "global" else config["driver_path"]

        self.caps = DesiredCapabilities.CHROME
        self.caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("--mute-audio")

        try:
            if not self.driver_path:
                self.driver = webdriver.Chrome(
                    options=self.options, desired_capabilities=self.caps)
            else:
                self.service = Service(self.driver_path)
                self.driver = webdriver.Chrome(
                    service=self.service, options=self.options, desired_capabilities=self.caps)
        except common.exceptions.SessionNotCreatedException as err:
            error_msg = '''
            Could not open chrome session please check the following
            1. Make sure you have chrome installed
            2. Make sure you have the correct driver for your chrome version with the correct version
            3. Make sure you have the correct driver path in the config file
            4. if the path is global make sure you have the driver in your system path
            5. if you still have problems you are welcome to open an issue on github
            '''
            color_print(error_msg, tcolors.FAIL)
            color_print(err.msg, tcolors.FAIL)
        except common.exceptions.WebDriverException as err:
            error_msg = '''
            Could not open chrome session please check the following
            1. Make sure you have the correct driver path in the config file
            2. if the path is global make sure you have the driver in your system path
            3. if you still have problems you are welcome to open an issue on github
            '''
            color_print(error_msg, tcolors.FAIL)
            color_print(err.msg, tcolors.FAIL)
            sys.exit(1)
            