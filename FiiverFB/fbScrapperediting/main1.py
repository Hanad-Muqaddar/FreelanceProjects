# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
import wget
import os
import requests
import re
import bs4
from tqdm import tqdm
from login_form import driver_return

# https://www.facebook.com/pepsi
# Create downloads folder
links=[]
if 'downloads' not in os.listdir():
    os.mkdir('downloads')

# check if the downloads folder is not empty. if it is not empty remove everything in it
if os.listdir('downloads'):
    for file in os.listdir('downloads'):
        os.remove('downloads/'+file)

def get_videos_edit(url):
    ''' Get list of facebook video post URLs'''
    driver = driver_return()
    driver.maximize_window()
    driver.delete_all_cookies()
    url = url+'/videos'
    driver.get(url)
    time.sleep(10)
    hrefs=[]
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
    time.sleep(2)
    
    try:
        accept_cookies_window = driver.find_element(By.XPATH, '//button[@title="Allow essential and optional cookies"]')
        accept_cookies_window.click()
    except:
        try:
            accept_cookies_window = driver.find_element(By.XPATH,
                                                        '/html/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]')
            accept_cookies_window.click()
        except:
            pass
    
    # Close Sign In Window
    try:
        close_sign_in = driver.find_element(By.XPATH,"//div[@aria-label='Close']")
        close_sign_in.click()
    except:
        pass
    
    SCROLL_PAUSE_TIME = 5
    last_height = driver.execute_script("return document.body.scrollHeight")
    # print(last_height)
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    spans = driver.find_elements(By.XPATH,"//span[@role='button']")
    if len(spans)!=0:
        for span in spans:
            # Storing attributes of href (video url)
            href = span.get_attribute('href')
            # print('href=',href)
            if href and not href.startswith('/'):
                # Convert to caseless string
                hrefs.append(href)
    else:
        # get all a tags with role='link'
        a_tags=driver.find_elements(By.XPATH,'//a[@role="link"]')
        for a in a_tags:
            # store the attribute href of the link
            href=a.get_attribute('href')
            # avoid urls starting '/' -> local references of videos, doesnt download videos
            if href and not href.startswith('/') and 'video' in href:
                # Convert to caseless string
                hrefs.append(href)
    final_hrefs = list(set(hrefs))
    # final_hrefs.pop(0)
    driver.close()
    return final_hrefs

def get_photos_edit(url):
    ''' Get list of facebook photo post URLs'''
    base_url = url
    # chrome_options = Options()
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver = driver_return()
    driver.maximize_window()
    url=url+'/photos'
    driver.get(url)
    time.sleep(10)
    hrefs=[]
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # Accept Cookies window
    try:
        accept_cookies_window = driver.find_element(By.XPATH, '//button[@title="Allow essential and optional cookies"]')
        accept_cookies_window.click()
    except:
        try:
            accept_cookies_window = driver.find_element(By.XPATH,
                                                        '/html/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]')
            accept_cookies_window.click()
        except:
            pass

    # Close Sign In Window
    try:
        close_sign_in = driver.find_element(By.XPATH,"//div[@aria-label='Close']")
        close_sign_in.click()
    except:
        pass
    
    SCROLL_PAUSE_TIME = 7
    last_height = driver.execute_script("return document.body.scrollHeight")
    # print(last_height)
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    time.sleep(5)
    
    a_tags = driver.find_elements(By.XPATH,"//a[@rel='theater']")
    a_tags.extend(driver.find_elements(By.XPATH,"//a[@role='link']"))
    # a_tags.extend(driver.find_elements(By.XPATH,"//div[@style='max-width: 300px; min-width: 210px;']//a[@role='link'] | //div[@style='margin:-4px -4px']//a[@role='link']"))
    # print('total a tags:',len(a_tags))
    for a in a_tags:
        # Storing attributes of href (photo url)
        href = a.get_attribute('href')
        if href:
            hrefs.append(href)
    final_photo_links = []
    for photo in hrefs:
        if "/photos/" in photo and photo != url:
            final_photo_links.append(photo)
        else:
            continue
    driver.quit()
    return final_photo_links

URLs=[]

def download_videos(urls, name):
    ''' Download videos from fbvideodown using URLs'''
    # driver=webdriver.Chrome(ChromeDriverManager().install())
    driver = driver_return()
    driver.maximize_window()
    driver.get("https://fdown.net/index.php")
    time.sleep(5)
    try:
        consent_button = driver.find_element(By.XPATH, "//button[@class='fc-button fc-cta-consent fc-primary-button']")
        consent_button.click()
    except:
        pass
    time.sleep(2)
    for url in tqdm(urls):
        try:
            # Get input box element with xpath //*[@id="function-area"]/div/div[1]/input
            # input_box = driver.find_element(By.XPATH,"//input[@class='form-control input-lg']")
            input_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@class='form-control input-lg']")))
            # Clear the input box
            input_box.clear()
            # Send the url to the input box
            input_box.send_keys(url)
            # Get element with xpath  //*[@id="function-area"]/div/div[2]
            download_button = driver.find_element(By.XPATH,"//button[@class='btn btn-primary input-lg']")
            time.sleep(3)
            # Click the button
            download_button.click()
            time.sleep(5)
            # Get element with xpath //*[@id="dl-area"]/div/div/video/source
            try:
                video = driver.find_element(By.XPATH,"//a[@id='hdlink']")
                # get the src attribute of the video element
                src = video.get_attribute('href')
            except:
                video = driver.find_element(By.XPATH, "//a[@id='sdlink']")
                src = video.get_attribute('href')
            # download the video
            if name not in os.listdir():
                try:
                    os.mkdir(f'downloads/{name}/')
                except:
                    pass
                try:
                    os.mkdir(f'downloads/{name}/videos')
                except:
                    pass
                wget.download(src, out=f'downloads/{name}/videos')
            print('downloaded:',src)
            time.sleep(5)
            driver.get("https://fdown.net/index.php")
            time.sleep(2)
            try:
                consent_button = driver.find_element(By.XPATH, "//button[@class='fc-button fc-cta-consent fc-primary-button']")
                consent_button.click()
            except:
                pass
            time.sleep(5)
        except Exception as e:
            driver.get("https://fdown.net/index.php")
            time.sleep(2)
            try:
                consent_button = driver.find_element(By.XPATH,
                                                     "//button[@class='fc-button fc-cta-consent fc-primary-button']")
                consent_button.click()
            except:
                pass
            time.sleep(5)
            print(e)
    driver.close()



def download_photos(urls, name):
    ''' Download photos from fbvideodown using URLs'''
    driver=webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.fbvideodown.com/download-facebook-photos.html')
    time.sleep(5)
    for url in tqdm(urls):
        try:
            # Get input box element with xpath //*[@id="function-area"]/div/div[1]/input
            input_box = driver.find_element(By.XPATH,"//*[@id='function-area']/div/div[1]/input")
            # Clear the input box
            input_box.clear()
            # Send the url to the input box
            input_box.send_keys(url)
            # Get element //*[@id="function-area"]/div/div[2]
            download_button = driver.find_element(By.XPATH,"//*[@id='function-area']/div/div[2]")
            # Click the button
            download_button.click()
            time.sleep(5)
            # Get img element with xpath //*[@id="dl-area"]/div/div/img
            img = driver.find_element(By.XPATH,"//*[@id='dl-area']/div/div/img")
            # Get the src attribute of the img element
            src = img.get_attribute('src')
            # Download the image
            wget.download(src, out=f'downloads/{name}/photos')
            print('downloaded:',src)
        except:
            print("Error: This video might be private")
            pass
    driver.quit()


def main():
    with open('urls.txt') as f:
        urls=f.readlines()


    for url in urls:
        url=url.strip()

        videos = get_videos_edit(url)
        # photos = get_photos_edit(url)
        name = url.split("/")[-1]
        print('total videos:',len(videos))
        download_videos(videos, name)
        # print('total photos:',len(photos))
        # download_photos(photos, name)


if __name__ == "__main__":
    main()