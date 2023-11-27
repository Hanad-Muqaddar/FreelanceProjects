import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from scrapy import Selector
from selenium.webdriver.common.by import By
import pandas as pd
from csv import DictWriter
import time
import os



class BrotjScript:

    def getPlugin(self, proxy_host, proxy_port, proxy_user, proxy_pass):
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
    
    
    proxyArgsList = [
                        {
                            'proxy_host': '',
                            'proxy_port': '',
                            'proxy_user': '',
                            'proxy_pass': '',
                        },
                        {
                            'proxy_host': '',
                            'proxy_port': '',
                            'proxy_user': '',
                            'proxy_pass': '',
                        },
                        {
                            'proxy_host': '',
                            'proxy_port': '',
                            'proxy_user': '',
                            'proxy_pass': '',
                        }
                ]
    def return_driver(self,):
        chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_extension(self.getPlugin(**random.choice(self.proxyArgsList)))
        # chromeOptions.add_argument('--incognito') 
        chromeOptions.add_argument("--no-sandbox")
        chromeOptions.add_argument('--profile-directory=Default')
        chromeOptions.add_argument("--start-maximized")
        chromeOptions.add_argument("disable-infobars")
        chromeOptions.add_argument("--lang=en")
        chromeOptions.add_argument("--enable-javascript")
        chromeOptions.add_argument("--enable-cookies")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chromeOptions)
        return driver
    
    def return_item(self, response):
        list_items = []
        total_items = response.xpath("//div[@class='installer-item']")
        for item in total_items:
            it = {}
            try:
                it['Distance'] = item.xpath("normalize-space(.//span[@class='distance'])").get()
            except:
                it['Distance'] = ""
            try:
                it['Title'] = item.xpath("normalize-space(.//div[@class='teaser-title'])").get()
            except:
                it['Title'] = ""
            try: 
                it['Address'] = item.xpath("normalize-space(.//div[@class='address-container'])").get()
            except:
                it['Address'] = ""
            try:
                it['PhoneNumber'] = item.xpath("normalize-space(.//div[@class='contact-button']/button/@data)").get().replace("tel:", "").strip()
            except:
                it['PhoneNumber'] = ""
            try:
                it['Email'] = item.xpath("normalize-space(.//button[@class='button-email']/@data)").get().replace("mailto:", "").strip()
            except:
                it['Email'] = ""
            list_items.append(it)
        return list_items
    
    def getting_cicties_list(self,):
        data = pd.read_csv("Cities_for_Scraping.csv")
        return list(data['Cities'])
    

    def items_data_saving(self, data):
        if os.path.exists("Items_Data.csv"):
            pass
        else:
            dataframe_1 = pd.DataFrame([{"Distance":"", "Title" : "", "Address" : "", "PhoneNumber" : "", "Email" : ""}])
            dataframe_1.to_csv("Items_Data.csv", index=False)
        field_names = ['Distance', 'Title', 'Address', 'PhoneNumber',"Email"]
        with open('Items_Data.csv', 'a', newline='') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            try:
                dictwriter_object.writerow(data)
                f_object.close()
            except:
                pass
    
    def passing_data(self, items_list):
        for item in items_list:
            self.items_data_saving(item)
        return
    
    def final_csv_save(self,):
        df = pd.read_csv("Items_Data.csv", encoding="ISO-8859-1")
        new_df = df.iloc[1:,:]
        new_df = new_df.drop_duplicates(subset = ['Distance', 'Title', 'Address', 'PhoneNumber',"Email"])
        new_df.to_csv("Final_Items_File.csv", index=False)
        os.remove("Items_Data.csv")
        return



object = BrotjScript()
driver = object.return_driver()
all_cities = object.getting_cicties_list()

for city in all_cities:
    url = f"https://www.broetje.de/de/fachhandwerker-finden#installer_q={city}&installer_r=50&installer_s=0"
    driver.get(url)
    try:
        driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]').click()
    except:
        pass
    time.sleep(10)
    response = Selector(text = driver.page_source.encode('utf-8'))
    items = object.return_item(response)
    object.passing_data(items)
    loop_number = response.xpath("(//li[@class='pagination-number'])[last()]/a/@aria-label").get()
    if loop_number == None:
        continue
    for i in range(1,int(loop_number)):
        url = f"https://www.broetje.de/de/fachhandwerker-finden#installer_q={city}&installer_r=50&installer_s={i}"
        driver.get(url)
        try:
            driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]').click()
        except:
            pass
        time.sleep(10)
        response = Selector(text = driver.page_source.encode('utf-8'))
        items = object.return_item(response)
        object.passing_data(items)
object.final_csv_save()