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
    scriptDirectory = pathlib.Path().absolute()
    chromeOptions.add_argument(f"user-data-dir={scriptDirectory}\\userdata")
    # chromeOptions.add_extension(getPlugin(**random.choice(proxyArgsList)))
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chromeOptions)
    return driver

def download_image(down_path, url, file_name, verbose=True):
    try:
        img_content = requests.get(url).content
        img_file = io.BytesIO(img_content)
        image = Image.open(img_file)
        file_pth = down_path + file_name
        with open(file_pth, 'wb') as file:
            image.save(file)
        if verbose == True:
            print(f'The image downloaded successfully.')
    except Exception as e:
        print(f'Unable to download image.')

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

def making_url(url):
    if "https://www.jumia.com.tn" in url:
        return url
    elif "https://www.jumia.com.tn" not in url:
        return "https://www.jumia.com.tn" + url


def get_product_links(response):
    product_links = response.xpath("//a[@class='core']/@href").getall()
    return product_links
     
def technical_data(response):
    article_number = 3
    try:
        for i in range(1,5):
            text = response.xpath(f"//section[@class='card aim -mtm -fs16']//article[{i}]//h2/text()").get()
            if "Descriptif technique" in text:
                article_number = i
                break
    except:
        pass        
    keys = response.xpath(f"//section[@class='card aim -mtm -fs16']//article[{article_number}]//li//span[@class='-b']/text()").getall()
    values = response.xpath(f"//section[@class='card aim -mtm -fs16']//article[{article_number}]//li/text()").getall()
    f_values = [clean(val.replace(":", "")) for val in values]
    f_keys = [clean(key) for key in keys]
    dictionary = dict(zip(f_keys, f_values))
    weight = ""
    for key,value in dictionary.items():
        if "Poids" in key:
            weight = value
            break
    return weight

def resize_img(img):
    lst = img.split("https://tn.jumia.is/unsafe/fit-in/")[1].split("/")
    lst[0] = "680x680"
    f_img = "/".join(lst)
    f_img = "https://tn.jumia.is/unsafe/fit-in/" + f_img
    return f_img

def extracting_data(response, img_dir):
    try:
        name = clean(response.xpath("normalize-space(//h1[@class='-fs20 -pts -pbxs'])").get())
    except:
        name = ""
    try:
        regular_price = clean(response.xpath("normalize-space(//div[@class='-hr -mtxs -pvs']//span[@class='-b -ltr -tal -fs24'])").get())
        regular_price = regular_price.split(" ")[0]
    except:
        regular_price = ""
    try:
        discounted_price = clean(response.xpath("normalize-space(//div[@class='-hr -mtxs -pvs']//span[@class='-tal -gy5 -lthr -fs16'])").get())
        discounted_price = discounted_price.split(" ")[0]
    except:
        discounted_price = ""
    try:
        details = clean(response.xpath("//meta[@property='og:description']/@content").get())
    except:
        details = ""
    try:
        product_url = clean(response.xpath("//meta[@property='og:url']/@content").get())
    except:
        product_url = ""
    try:
        primary_images = list(set(response.xpath("//div[@class='-ptxs -pbs']//div[contains(@id,'imgs')]//img/@data-src").getall()))
        primary_images = '|'.join(primary_images)
    except:
        primary_images = ""
    try:
        breadcrums = response.xpath("//div[@class='brcbs col16 -pts -pbm']//a[@class='cbs']/text()").getall()
        f_breadcrums = [clean(bred) for bred in breadcrums]
        f_breadcrums = "|".join(f_breadcrums)
    except:
        f_breadcrums = []
    try:
        main_characteristics = response.xpath("//section[@class='card aim -mtm -fs16']//article[1]//div[@class='markup -pam']//li")
        chear_data = [clean(i.xpath("normalize-space()").get()) for i in main_characteristics]
        characteristics = "\n".join(chear_data)
    except:
        characteristics = ""
    try:
        weight = technical_data(response)
    except:
        weight = ""
    try:    
        primary_image = clean(response.xpath("//meta[@property='og:image']/@content").get())
    except:
        primary_image = ""
    primary_image = resize_img(primary_image)
    file_name = name.replace(" ","_") + ".jpg"
    download_image(img_dir, primary_image, file_name)
    
    item = {}
    item['Product_Name'] = name
    item['Regular_Price'] = regular_price
    item['Orignal_Price'] = discounted_price
    item['Details'] = details
    item['Product_Url'] = product_url
    item['Primary_Image'] = primary_images
    item['Breadcrums'] = f_breadcrums
    item['Main_Characteristics'] = characteristics
    item['Weight'] = weight
    return item
  
def resturant_data_saving(data):
    if os.path.exists("Products_Data.csv"):
        pass
    else:
        dataframe_1 = pd.DataFrame([{"Product_Name":"", "Regular_Price" : "", "Orignal_Price" : "", "Details" : "", "Product_Url" : "", "Primary_Image" : "", "Breadcrums" : "","Main_Characteristics" : "","Weight" : ""}])
        dataframe_1.to_csv("Products_Data.csv", index=False)
    field_names = ['Product_Name', 'Regular_Price', 'Orignal_Price', 'Details',"Product_Url", "Primary_Image", "Breadcrums", "Main_Characteristics", "Weight"]
    with open('Products_Data.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        try:
            dictwriter_object.writerow(data)
            f_object.close()
        except:
            pass
        
def product_links_saving(data):
    if os.path.exists("Product_Links.csv"):
        pass
    else:
        dataframe_1 = pd.DataFrame([{"Product_Links":""}])
        dataframe_1.to_csv("Product_Links.csv", index=False)
    field_names = ['Product_Links']
    with open('Product_Links.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        dictwriter_object.writerow(data)
        f_object.close()

def getting_unique_urls():
    if os.path.exists("Product_Links.csv"):
        pass
    else:
        dataframe_1 = pd.DataFrame([{"Product_Links":""}])
        dataframe_1.to_csv("Product_Links.csv", index=False)
    read_dataframe = pd.read_csv("Product_Links.csv")
    Unique_resturants_urls = read_dataframe['Product_Links'].to_list()
    return Unique_resturants_urls
      
def get_product(driver, product_urls, img_dir):
    for prod_url in product_urls:
        crawled_urls = getting_unique_urls()
        url = making_url(prod_url)
        if url in crawled_urls:
            continue
        else:
            data = {'Product_Links' : url}
            product_links_saving(data)
            driver.get(url)
            time.sleep(1)
            prod_response = Selector(text = driver.page_source.encode('utf-8'))
            product_data = extracting_data(prod_response, img_dir)
            resturant_data_saving(product_data)
    return

       
if __name__ == "__main__":
    
    images_download_directory = "C:/Users/Lenovo/Desktop/Five_Proj/Jumia/Images/"
     
    site_url = "https://www.jumia.com.tn/"
    driver = driver_return()
    driver.maximize_window()
    driver.get(site_url)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)
    driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")
    response = Selector(text = driver.page_source.encode('utf-8'))
    all_links = list(set(response.xpath("//a[@role='menuitem']/@href").getall()))
    for i in all_links:
        f_link = making_url(i)
        driver.get(f_link)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")
        response1 = Selector(text = driver.page_source.encode('utf-8'))
        product_links = get_product_links(response1)
        get_product(driver, product_links, images_download_directory)      
        while True:
            next_page_link = response1.xpath("//a[@aria-label='Page suivante']/@href").get()
            if next_page_link:
                next_page = making_url(next_page_link)
                driver.get(next_page)
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(1)
                driver.execute_script("window.scrollTo(document.body.scrollHeight,0)")
                response1 = Selector(text = driver.page_source.encode('utf-8'))
                product_links = get_product_links(response1)
                get_product(driver, product_links, images_download_directory)
            else:
                break
                
        
    
    
         
        


