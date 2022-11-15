from imghdr import tests
from unittest import TestCase
from urllib import response
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from scrapy import Selector
import zipfile
import pathlib
import random
import pandas as pd
import json
import re
import time
import os.path
from csv import DictWriter

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
                        # {
                        #     'proxy_host': 'de.proxymesh.com',
                        #     'proxy_port': '31280',
                        #     'proxy_user': '',
                        #     'proxy_pass': '',
                        # },
                        # {
                        #     'proxy_host': 'jp.proxymesh.com',
                        #     'proxy_port': '31280',
                        #     'proxy_user': '',
                        #     'proxy_pass': '',
                        # },
                        # {
                        #     'proxy_host': 'fr.proxymesh.com',
                        #     'proxy_port': '31280',
                        #     'proxy_user': '',
                        #     'proxy_pass': '',
                        # }
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
    # scriptDirectory = pathlib.Path().absolute()
    # chromeOptions.add_argument(f"user-data-dir={scriptDirectory}\\userdata") 
    # chromeOptions.add_extension(getPlugin(**random.choice(proxyArgsList)))
    # chromeOptions.add_argument('--incognito') 
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chromeOptions)
    return driver

def get_phone_number(text):
    phoneNumRegex = re.compile(r'"allergenPhoneNumber":"\d\d\d\d\d\d\d\d\d\d\d"')
    mo1 = phoneNumRegex.search(text)
    phone_number = mo1.group(0)
    phone_number = phone_number.replace('"allergenPhoneNumber":', "")
    return phone_number

def resturant_data_saving(data):
    if os.path.exists("Resturants_Data.csv"):
        pass
    else:
        dataframe_1 = pd.DataFrame([{"Resturant_Name":"", "Cusine" : "", "Address" : "", "Phone_Number" : ""}])
        dataframe_1.to_csv("Resturants_Data.csv", index=False)
    field_names = ['Resturant_Name', 'Cusine', 'Address', 'Phone_Number']
    with open('Resturants_Data.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        dictwriter_object.writerow(data)
        f_object.close()
    return

def _sanitize(input_val):
    pattern_re = r'\s+'
    repl_re = ' '
    return re.sub(pattern_re, repl_re, input_val, flags=0).strip()


def clean(lst_or_str):
    if not isinstance(lst_or_str, str) and getattr(
        lst_or_str, '__iter__', False
    ):  # if iterable and not a string like
        return [x for x in (_sanitize(y) for y in lst_or_str if y is not None) if x]
    return _sanitize(lst_or_str) if lst_or_str else None

def getting_unique_urls():
    read_dataframe = pd.read_csv("Links.csv")
    Unique_resturants_urls = read_dataframe['Resturant_Links'].to_list()
    return Unique_resturants_urls

def extracting_data(response):
    item = {}
    try:
        name = clean(response.xpath("//h1[@data-test-id='restaurant-heading']/text()").get())
    except:
        name = ""
    try:
        cusines = clean(response.xpath("normalize-space(//p[@data-js-test='header-cuisines'])").get())
    except:
        cusines = ""
    try:
        address = clean(response.xpath("normalize-space(//p[@class='l-centered c-restaurantHeader-address'])").get())
    except:
        address = ""
    raw_text_for_number = response.xpath("//script[@data-vmid='load-fonts']/following-sibling::script").get()
    try:
        phone_number = clean(get_phone_number(raw_text_for_number))
    except:
        phone_number = ""
    item['Resturant_Name'] = name
    item['Cusine'] = cusines
    item['Address'] = address
    item['Phone_Number'] = phone_number
    return item

def making_url(url):
    if "https://www.just-eat.co.uk" in url:
        return url
    elif "https://www.just-eat.co.uk" not in url:
        return "https://www.just-eat.co.uk" + url


if __name__ == "__main__":
    
    BASE_URL = "https://www.just-eat.co.uk"
    Unique_resturants_urls = []
    r_urls= []
    if os.path.exists("Links.csv"):
        Unique_resturants_urls = getting_unique_urls() 
    else:
        dataframe_1 = pd.DataFrame({"Resturant_Links":[]})
        dataframe_1.to_csv("Links.csv")
    driver = driver_return()
    driver.maximize_window()
    driver.get("https://www.just-eat.co.uk/takeaway")
    response = Selector(text = driver.page_source.encode('utf-8'))
    location_links = response.xpath('//h2[contains(text(), "Find Takeaways in other locations")]/following-sibling::div//li[@class="link-item"]/a/@href').getall()
    for link in location_links:
        final_link = making_url(link)
        try:
            driver.get(final_link)
        except:
            continue
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")
        response2 = Selector(text = driver.page_source.encode('utf-8'))
        resturants_links = response2.xpath("//a[@data-test-id='restaurant']/@href").getall()
        for i in resturants_links:
            if i not in Unique_resturants_urls:
                final_link1 = making_url(i)
                try:
                    driver.get(final_link1)
                except:
                    continue
                r_urls.append(i)
                response3 = Selector(text = driver.page_source.encode('utf-8'))
                data_to_store = extracting_data(response3)
                resturant_data_saving(data_to_store)
                if len(r_urls) == 20:
                    df1 = pd.read_csv("Links.csv")
                    df2 = pd.DataFrame({"Resturant_Links":r_urls})
                    df3 = pd.concat([df1, df2], ignore_index=True)
                    df3.to_csv("Links.csv", index=False)
                    Unique_resturants_urls = getting_unique_urls()
                    r_urls = []
            else:
                continue
    
    
    
         
        


