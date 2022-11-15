from lib2to3.pgen2 import driver
from msilib.schema import Directory
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import zipfile
import pathlib
from datetime import datetime as dt
from selenium.webdriver.common.by import By

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
    scriptDirectory = pathlib.Path().absolute()
    chromeOptions.add_argument(f"user-data-dir={scriptDirectory}\\userdata")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chromeOptions)
    return driver

def login():
    driver = driver_return()
    driver.maximize_window()
    driver.get("https://studio.youtube.com")
    while True:
        d = input("Enter Quit to stop")
        if d.lower() == "quit":
            break 
        continue
    driver.close()

# login()