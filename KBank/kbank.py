import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pathlib
import time
from scrapy import Selector
import json


def saving_to_json(my_dict):
    with open("KBANK_Data.json", "w") as outfile:
        json.dump(my_dict, outfile)

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
    # chromeOptions.add_argument(f"user-data-dir={scriptDirectory}\\userdata")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chromeOptions)
    return driver

def parse_data(response, recent_transacrion_path):
    avilable_balance = response.xpath('normalize-space((//app-account-user-details//table/tbody//tr//td)[1]//span)').get()
    trans = response.xpath(recent_transacrion_path)
    transactions = []
    for my_class in trans:
        dict_data = {}
        try:
            dict_data['Transaction_Date'] = my_class.xpath('normalize-space(((.//div[contains(@class,"list")])[1]//p)[2])').get()
        except:
            dict_data['Transaction_Date'] = ""
        try:
            dict_data['List_recieve_or_send'] = my_class.xpath('normalize-space(((.//div[contains(@class,"list")])[2]//p)[2])').get()
        except:
            dict_data['List_recieve_or_send'] = ""
        try:
            dict_data['Withdraw'] = my_class.xpath('normalize-space(((.//div[contains(@class,"list")])[3]//p)[2])').get()
        except:
            dict_data['Withdraw'] = ""
        try:
            dict_data['Deposit'] = my_class.xpath('normalize-space(((.//div[contains(@class,"list")])[4]//p)[2])').get()
        except:
            dict_data['Deposit'] = ""
        try:
            dict_data['Details'] = my_class.xpath('normalize-space(((.//div[contains(@class,"list")])[5]//p)[2])').get()
        except:
            dict_data['Details'] = ""
        try:
            dict_data['Funnel'] = my_class.xpath('normalize-space(((.//div[contains(@class,"list")])[6]//p)[2])').get()
        except :
            dict_data['Funnel'] = ""
        transactions.append(dict_data)
    final_dictioanry = {"Avialble_Balance":avilable_balance, "Transactions" : transactions}
    return final_dictioanry

# #################################################################################################################
# #################################################################################################################
# #################################################################################################################
# #################################################################################################################
# #################################################################################################################

user_name = "Jaray2499"
password = "Raywat@2499!@#$"
user_name_xpath = '//input[@name="userName"]'
password_xpath = '//input[@name="password"]'
login_button_xpath = '//a[@id="loginBtn"]'
view_account_details_xpath = '//app-account-summary-card//a[@class="a-center pointer"]'
search_button_xpath = '//a[@class="btn btn-small hv-icon searchBtn btn-dark-blue"]'
main_url = "https://online.kasikornbankgroup.com/kbiz/"
recent_transaction_xpath = '//div[@class="non-table-04"]//div[@class="bottom"]//div[contains(@class,"lists") and not(contains(@class,"recent-transaction-non-tabel-detail")) and not(contains(@class,"sc-paginations"))]'


driver = driver_return()
driver.maximize_window()
driver.get(main_url)
time.sleep(10)
try:
    user_name = driver.find_element(By.XPATH, user_name_xpath)
    user_name.send_keys(user_name)
    password = driver.find_element(By.XPATH, password_xpath)
    password.send_keys(password)
    login_button = driver.find_element(By.XPATH, login_button_xpath)
    login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
    login_button.click()
except:
    pass
time.sleep(5)

view_account_details = driver.find_element(By.XPATH, view_account_details_xpath)
view_account_details = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, view_account_details_xpath)))
view_account_details.click()


search_button = driver.find_element(By.XPATH, search_button_xpath)
search_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, search_button_xpath)))
search_button.click()
# driver.close()
time.sleep(5)

response = Selector(text = driver.page_source.encode('utf-8'))

outcome = parse_data(response, recent_transaction_xpath)
print("**********************************")
print("**********************************")
saving_to_json(outcome)
print("**********************************")
print("**********************************")

 
