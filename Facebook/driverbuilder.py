import os
import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from passwordprompt import PasswordPrompt
from dataextractor import DataExtractor


class DriverBuilder:
    
    def __init__(self, configparser):
        self._configparser = configparser

    def passwordprompt(self):
        self._password = PasswordPrompt().prompt()

        return self

    def buildchrome(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        if self._configparser.headless_chrome:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument('--log-level=3')

        self._driver = webdriver.Chrome(
            executable_path=self._configparser.driver_path, options=chrome_options)

        self._driver.set_page_load_timeout(self._configparser.request_timeout)

        return self

    def facebooklogin(self):
        self._driver.get("https://www.facebook.com")

        email_box = self._driver.find_element_by_id("email")
        email_box.send_keys(self._configparser.facebook_login)

        password_box = self._driver.find_element_by_id("pass")
        password_box.send_keys(self._password)

        login_box = self._driver.find_element_by_id("u_0_b")
        login_box.click()

        return self

    def visitgroup(self):
        self._driver.get(
            "https://www.facebook.com/groups/{0}".format(self._configparser.group_name))

        return self

    def scroll(self):
        for _ in range(self._configparser.number_of_scrolls):
            self._driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(self._configparser.scroll_timeout)

        return self

    def create_output_folder(self, foldername):
        self._output_folder = foldername
        os.mkdir(self._output_folder)

        return self

    def extractdata(self):
        elements = self._driver.find_elements_by_xpath(
            "//div[contains(text(), '$')]")

        return DataExtractor(elements, self._output_folder).extract()

    def sleep(self):
        sleep(self._configparser.waiting_time)

        return self
