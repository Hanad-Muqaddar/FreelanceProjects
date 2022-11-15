from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date, datetime, timedelta
import properties as prop
import time
import sys, os


def export_handler():
    try:


        userId = "YASHROADLINES"
        userPass = "Yash@1234"
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

        # chrome_path = prop.driver_path
        options = webdriver.ChromeOptions()
        prefs = {'download.default_directory' : prop.download_path}
        options.add_argument('log-level=3')
        options.add_experimental_option('prefs', prefs)
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        urlName = "https://fastaglogin.icicibank.com/CUSTLOGIN/Default.aspx"
        try:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=options, desired_capabilities=capa)
        except Exception as e:
            print(e)
        driver.maximize_window()
        driver.get(urlName)
        time.sleep(3)



        time.sleep(2)
        ##
        try:
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="rdCorporateLogin"]')).click()
        except TimeoutException:
            pass

        time.sleep(5)
        try:
            driver.execute_script("document.getElementById('txtUserId1').value=arguments[0]", userId)
            driver.execute_script("document.getElementById('txtPassword1').value=arguments[0]", userPass)
            WebDriverWait(driver, 3).until(lambda x: x.find_element_by_xpath('//*[@id="btnLoginCorporate"]').click())
        except:
            pass

        try:
            # //*[@id="lblMessagecrp"]
            invalid_text = driver.find_element_by_xpath('//*[@id="lblMessagecrp"]').text
        except Exception as e:
            pass
        time.sleep(1)
        if invalid_text == 'Invalid Credentials':
            prop.invalid_credentilas_flag = True
            driver.close()
            print("XXXXXXXXXXXX Invalid Credentials XXXXXXXXXXXXXXX")
        else:
        ### For already session pop-up
            try:
                WebDriverWait(driver, 3).until(lambda x: x.find_element_by_xpath('//*[@id="btnYes"]').click())
            except Exception as e:
                print(e)
                pass

            driver.get('https://fastaglogin.icicibank.com/CUSTLOGIN/Pages/Documents/AdHocStatements.aspx')
            time.sleep(3)


            try:
                download_link = driver.find_element_by_link_text('Export Transaction Summary to Excel')
                download_link.click()
            except Exception as e:
                print(e)
                pass

            ## download logic
            while not dl_wait:
                time.sleep(5)
                for fname in os.listdir(prop.download_path):
                    if not fname.endswith('.crdownload'):
                        dl_wait = True
            time.sleep(5)

            ## For logout click
            try:
                WebDriverWait(driver, 5).until(
                    lambda x: x.find_element_by_xpath('//*[@id="lnkbtn"]')).click()
                time.sleep(3)
            except Exception as e:
                print(e)
                pass
        print("~~~~~~~~~Export handler processed successfully.~~~~~~~~~~~")
        driver.close()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        error_value = str(exc_type)+','+str(fname)+','+str(exc_tb.tb_lineno)
        # prop.logger.error(error_value)

if __name__  ==  "__main__":
    export_handler()
