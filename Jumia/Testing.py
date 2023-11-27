from msilib.schema import Directory
import requests
from urllib import response
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from scrapy import Selector
import zipfile
import pathlib
import pandas as pd
import re
import time
import os.path
from csv import DictWriter
import io
from datetime import datetime as dt
from PIL import Image
import time
from selenium.webdriver.common.by import By
import random

names_list = []

def getPlugin(proxy_host, proxy_port, proxy_user, proxy_pass):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
 
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };
 
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
 
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
 
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (proxy_host, proxy_port, proxy_user, proxy_pass)
    pluginfile = 'proxy_auth_plugin.zip'
 
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    
    return pluginfile
 

def driver_return():
    proxyArgsList = [
                        {
                            'proxy_host': 'au.proxymesh.com',
                            'proxy_port': '31280',
                            'proxy_user': 'waleeProxy',
                            'proxy_pass': 'Cheeta@1',
                        },
                ]

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--window-size=150,500")
    chromeOptions.add_argument("--disable-automation")
    chromeOptions.add_argument("--no-sandbox")
    chromeOptions.add_argument('--profile-directory=Default')
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument("disable-infobars")
    chromeOptions.add_argument("--lang=en")
    chromeOptions.add_argument("--enable-javascript")
    chromeOptions.add_argument("--enable-cookies")
    chromeOptions.add_experimental_option("detach", True)
    # scriptDirectory = pathlib.Path().absolute()
    # chromeOptions.add_argument(f"user-data-dir={scriptDirectory}\\userdata")
    chromeOptions.add_extension(getPlugin(**random.choice(proxyArgsList)))
    driver = webdriver.Chrome(service=ChromeService("C:/Users/HP/Desktop/Journaya/chromedriver.exe"), options=chromeOptions)
    return driver


site_url = "https://whatismyipaddress.com/"
# site_url = "https://www.westernunion.com/us/en/currency-converter/usd-to-pkr-rate.html"
driver = driver_return()
driver.maximize_window()
driver.get(site_url)
