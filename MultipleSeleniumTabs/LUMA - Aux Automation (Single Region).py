import sys
import time
import os
import json
import random
import string
import xlrd
import csv
import selenium
import pandas as pd
from datetime import datetime
from selenium import webdriver as uc
#import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Dict, List
try:
    os.mkdir("DownloadFiles")
except:
    pass

# Global veriables
LOGIN_PAGE = "https://prep-luma.lumapr.com/prepaGD/login/auth?format="
DOWNLOAD_PAGE = "https://prep-luma.lumapr.com/prepaGD/employeeHome/monitorCases"
BUSCAR_PAGE = "https://prep-luma.lumapr.com/prepaGD/search/formSearch"


user= ""
pas= ""
waitingTime = 120 # seconds
waitingSearch = 20 # seconds to wait after search btn clicked
region_option = "REGION DE CAGUAS"
agent_option = "" # by value

# XPATHs

USER_XPATH = "//input[@id='username']"
PASS_XPATH = "//input[@id='password']"
SUBMIT_XPATH = "//input[@type='submit']"
FILTER_XPATH = "//select[@id='region']"
SEARCH_BTN = "//input[@type='submit']"
H3_PGE = "//h3[text()='Monitoreo de Proyectos']"
EXCEL_DOWNLOAD = "//a[contains(@class,'btn btn-default')]"

NUMBERS_XPATH = "//label[@for='accountNumber']/following-sibling::input[1]"
BUSCAR_XPATH = "//input[@class='btn btn-primary']"
CHECK_RESULT ="//td[text()='Estudio']"
ASIGNAR_XPATH = "(//table[@id='search-result-tbl']//a)[2][text()='Asignar a Auxiliar para evaluación']"

ASGN_PAGE_XPATH = "//h3[text()[normalize-space()='Asignar a Auxiliar para evaluación']]"
FILTER_ASSGN_XPATH = "//select[@id='auxiliarEstudio']"
COMPLETE_XPATH = "//input[@class='btn btn-primary']"
FINAL_CHECK = "//h3[text()[normalize-space()='Proceso de Estudio']]"
ERROR_CHECK= "//div[@class='error-title']"



def waitForItem(driver, selector_type, selector_value, timeout=20, logging=False):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((selector_type, selector_value)))
    except selenium.common.exceptions.TimeoutException:
        if logging:
            print(
                f" > Timeout error: Element couldn't be located. ({selector_value})")
        return None
    return element

def xlsxReaderReturnListNumbers(filename):
    sheet = xlrd.open_workbook(filename).sheet_by_index(0)

    # writer object is created
    col = csv.writer(open("temp.csv",
                        'w',
                        newline="",encoding='utf-8'))

    # writing the data into csv file
    for row in range(sheet.nrows):
        # row by row write
        # operation is perform
        col.writerow(sheet.row_values(row))

    # read csv file and convert
    # into a dataframe object
    df = pd.DataFrame(pd.read_csv("temp.csv"))
    df=df.loc[df['Tareas'] == 'Asignar a Auxiliar de Estudio']
    return df['Número de Cuenta'].tolist()


def excelFileDownloader(driver):
    driver.get(DOWNLOAD_PAGE)
    time.sleep(5)
    filter_check= waitForItem(driver, By.XPATH, H3_PGE, timeout=waitingTime)
    if filter_check:
        time.sleep(1)
        select = Select(driver.find_element(By.XPATH,FILTER_XPATH))
        select.select_by_visible_text(region_option)
        time.sleep(1)
        driver.find_element(By.XPATH,SEARCH_BTN).click()
        for i in reversed(range(waitingSearch)):
            print("\r Waiting for [%d] Seconds "%i,end="")
            time.sleep(1)
        driver.find_element(By.XPATH,EXCEL_DOWNLOAD).click()
        time.sleep(2)
        return True
    else:
        return False

def numbersInsertor(driver,number):
    driver.get(BUSCAR_PAGE)
    time.sleep(3)
    numbersInp = waitForItem(driver, By.XPATH, NUMBERS_XPATH, timeout=30)
    if numbersInp:
        numbersInp.send_keys(number)
        time.sleep(1)
        driver.find_element(By.XPATH,BUSCAR_XPATH).click()
        time.sleep(2)
        resultcheck = waitForItem(driver, By.XPATH, CHECK_RESULT, timeout=30)
        if resultcheck:
            assignBtn = waitForItem(driver, By.XPATH, ASIGNAR_XPATH, timeout=2)
            if assignBtn:
                assignBtn.click()
                time.sleep(3)
                if waitForItem(driver, By.XPATH, ASGN_PAGE_XPATH, timeout=30):
                    select = Select(driver.find_element(By.XPATH,FILTER_ASSGN_XPATH))
                    select.select_by_value(agent_option)
                    time.sleep(1)
                    driver.find_element(By.XPATH,COMPLETE_XPATH).click()
                    time.sleep(2)
                    lastcheck = waitForItem(driver, By.XPATH, ERROR_CHECK, timeout=7)
                    if lastcheck:
                        print(f" [Info] Successfully Added Number {number}")
                        return True
                    else:
                        if "Incapsula incident ID" in driver.page_source:
                            print(f" [Info] Successfully Added Number {number}")
                            return True
                        else:
                            lastcheck=waitForItem(driver, By.XPATH, FINAL_CHECK ,timeout=50)
                            if lastcheck:
                                print(f" [Info] Successfully Added Number {number}")
                                return True

    return False



def loginWebsite(driver):
    driver.get(LOGIN_PAGE)
    time.sleep(5)
    usrInputChk = waitForItem(driver, By.XPATH, USER_XPATH, timeout=30)
    if usrInputChk:
        usrInputChk.send_keys(user)
        time.sleep(1)
        driver.find_element(By.XPATH,PASS_XPATH).send_keys(pas)
        time.sleep(1)
        driver.find_element(By.XPATH,SUBMIT_XPATH).click()
        time.sleep(2)
        return True
    else:
        return False




def driver_init_Chrome():
    chrome_options = uc.ChromeOptions()
    prefs = {'download.default_directory': '{}\{}\\'.format(os.getcwd(),"DownloadFiles")}
    chrome_options.add_experimental_option('prefs', prefs)
    # chrome_options.add_argument("--user-data-dir=C:\\Users\\Seroxis\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
    driver = uc.Chrome(options=chrome_options,service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    return driver

def returnFiletoList(filename):
    with open(filename, "r") as f:
        LinesToList = f.read().strip().split("\n")
    return LinesToList


def domain_to_url(domain: str) -> str:
    if domain.startswith("."):
        domain = "www" + domain
    return "http://" + domain

def login_using_cookie_file(driver: WebDriver, cookie_file: str):
    """Restore auth cookies from a file. Does not guarantee that the user is logged in afterwards.
    Visits the domains specified in the cookies to set them, the previous page is not restored."""
    domain_cookies: Dict[str, List[object]] = {}
    with open(cookie_file) as file:
        cookies: List = json.load(file)
        # Sort cookies by domain, because we need to visit to domain to add cookies
        for cookie in cookies:
            try:
                domain_cookies[cookie["domain"]].append(cookie)
            except KeyError:
                domain_cookies[cookie["domain"]] = [cookie]

    for domain, cookies in domain_cookies.items():
        driver.get(domain_to_url(domain + "/robots.txt"))
        for cookie in cookies:
            cookie.pop("sameSite", None)  # Attribute should be available in Selenium >4
            cookie.pop("storeId", None)  # Firefox container attribute
            try:
                driver.add_cookie(cookie)
            except:
                print(f"Couldn't set cookie {cookie['name']} for {domain}")
    return True


if __name__ == '__main__':
    start_time = datetime.now()
    masterCounter=0
    allfilesBefore = os.listdir("DownloadFiles")
    driver=driver_init_Chrome()
    if login_using_cookie_file(driver,'cookies.txt'):
        listofNumbers=returnFiletoList("numbersList.txt")
        if len(listofNumbers)>0:
            for number in listofNumbers:
                if numbersInsertor(driver,int(number)):
                    masterCounter+=1
                    t = time.strftime("%I:%M %p")
                    print(f"{t} - {int(number)} Number Uploaded Successfully | {len(listofNumbers)}/{masterCounter} numbers uploaded")
                    time.sleep(2)
                else:
                    t = time.strftime("%I:%M %p")
                    print(f"{t} - {int(number)} Number already uploaded (Asignar to Auxiliar not shown)")
    else:
        print(" [Info] Login Page Not Loaded")
        sys.exit()
    end_time = datetime.now()
    t = time.strftime("%I:%M %p")
    print(f"{t} - {len(listofNumbers)}/{masterCounter} numbers uploaded, time elapsed {end_time - start_time}")