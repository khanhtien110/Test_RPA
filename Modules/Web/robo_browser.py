from RPA.Browser.Selenium import SeleniumLibrary
from robocorp.tasks import task
from Modules.TrackAndTrace import RPATracker
from RPA.Desktop import Desktop
from RPA.Browser.Playwright import Playwright
import os

import time


# --disable-features=AutomaticHttps
class RoboBrowser:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # If no instance exists, create it
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_data, rpa_tracker):
        if not hasattr(self, "initialized"):
            # Ensure the object is only initialized once
            selenium = SeleniumLibrary()
            desk = Desktop()
            self.browser_engine = config_data.get("browser_engine", "gc")
            self.initialized = True  # Mark the object as initialized
            self.robo_browser = selenium
            self.robo_desktop = desk
            self.rpa_tracker = rpa_tracker
            self.data = config_data
            self.browser_options = config_data.get("browser_options")

    def cleanup_browser(self):
        self.robo_browser.close_browser()

    def handle_redirect_https(self):
        #://flags/#edge-automatic-https
        pass
    
    def handle_login(self):
        is_successful = False
        browser_options = "add_argument('--disabled-features=AutomaticHttps')"
        # browser_options = "add_argument('--disable-popup-blocking')"
        try:
            self.robo_browser.open_browser(browser=self.browser_engine)

            self.robo_browser.maximize_browser_window()

            self.rpa_tracker.track("Input username")
            # for input id
            self.robo_browser.input_text(
                self.data["username_selector"], self.data["id"]
            )

            self.rpa_tracker.track("Input password")
            # for input password
            self.robo_browser.input_text(
                self.data["password_selector"], self.data["pw"]
            )

            self.rpa_tracker.track("Click Login button")
            # handle click
            self.robo_browser.click_button(self.data["btnLogin_selector"])
            # self.robo_desktop.click("alias:btnLogin")

            check_success = self.find_element(self.data["check_login_success"])
            is_successful = True
            self.rpa_tracker.info("Logged in sucessfully")
        except Exception as e:
            self.rpa_tracker.error("Login failed. " + e.args[0])

        return is_successful

    def handle_logout(self):
        is_successful = False
        try:

            self.rpa_tracker.track("Click Logged out button")
            self.robo_browser.click_element(self.data["btnLogout_selector"])
            check_success = self.find_element(self.data["check_logout_success"])
            is_successful = True
            self.rpa_tracker.info("Logged out successfully.")
        except Exception as e:
            self.rpa_tracker.error("Failed to logout. " + e.args[0])

        return is_successful

    def find_element(self, locator):
        element = None
        try:
            element = self.robo_browser.find_element(locator)
        except Exception as e:
            self.rpa_tracker.eror("Error when finding element. " + e.args[0])

        return element
