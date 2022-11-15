from browser_user_login import driver_return
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import Selector
from csv import DictWriter
import pandas as pd
import nltk
from nltk.corpus import stopwords
import requests
import os
import wget
import time
import glob
import re
import json
import random

# Create downloads folder
if 'downloads' not in os.listdir():
    os.mkdir('downloads')

# check if the downloads folder is not empty. if it is not empty remove everything in it
def Remove_everything_from_folder():
    if os.listdir('downloads'):
        for file in os.listdir('downloads'):
            os.remove('downloads/'+file)
    return
Remove_everything_from_folder()

def _sanitize(input_val):
    # pattern_re = r'\s+[^A-Za-z0-9]+ '
    pattern_re = r'[^a-zA-Z0-9]+ '
    repl_re = ' '
    str1 = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1', input_val)
    return re.sub(pattern_re, repl_re, str1, flags=0).strip()


def clean(lst_or_str):
    if not isinstance(lst_or_str, str) and getattr(
        lst_or_str, '__iter__', False
    ):  # if iterable and not a string like
        return [x for x in (_sanitize(y) for y in lst_or_str if y is not None) if x]
    return _sanitize(lst_or_str) if lst_or_str else None

def clear_field(field, system):
    field.click()
    time.sleep(5)
    if system == "mac":
        field.send_keys(Keys.COMMAND + 'a')
    else:
        field.send_keys(Keys.CONTROL + 'a')
    time.sleep(5)
    field.send_keys(Keys.BACKSPACE)
    return

def write_in_field(field, string, select_all=False):
		if select_all:
			clear_field(field, "not_mac")
		else:
			field.click()
			time.sleep(5)
		field.send_keys(string)


# Uploading video to youtube.
def uploading_video(video_path, title, description, tags):
    driver = driver_return()
    driver.maximize_window()
    driver.get("https://studio.youtube.com")
    time.sleep(5)
    upload_button = driver.find_element(By.XPATH, '//*[@id="upload-icon"]')
    upload_button.click()
    time.sleep(5)
    file_input = driver.find_element(By.XPATH, '//*[@id="content"]/input')
    file_input.send_keys(video_path)
    time.sleep(20)
    title_field, description_field = driver.find_elements(By.ID, "textbox")
    write_in_field(title_field, title, select_all=True)
    write_in_field(description_field, description, select_all=True)
    time.sleep(5)
    driver.find_element(By.ID, 'toggle-button').click()
    time.sleep(5)
    tags_container = driver.find_element(By.ID, "tags-container")
    tags_field = driver.find_element(By.ID, "text-input")
    write_in_field(tags_field, ','.join(tags))
    next_button = driver.find_element(By.XPATH, '//*[@id="next-button"]')
    for i in range(3):
        next_button.click()
        time.sleep(5)
    done_button = driver.find_element(By.XPATH, '//*[@id="done-button"]')
    done_button.click()
    time.sleep(5)
    driver.close()
    


# This function is downloading files.
def download(src):
    wget.download(src, out=f'downloads')
    return

# This function is getting 
def getting_video_links(url):
    result = requests.get(url)
    response = Selector(result)
    links = response.css(".entry-title a ::attr(href)").getall()
    return links

def parse_description(response):
    desc = response.xpath("//div[@class='entry-content']/p")
    total_content = []
    for i in desc:
        text = i.xpath('normalize-space()').get()
        total_content.append(text)
    description = ",".join(total_content)
    f_desc = clean(description)
    return f_desc

def writing_json_file(dic, path):
    with open(f"{path}/data.json", "w") as outfile:
        outfile.write(dic)
    return

def making_tags(in_text):
    nltk.download("stopwords")
    stop = set(stopwords.words("english"))
    filtered_words = [word.lower() for word in in_text.split() if word.lower() not in stop]
    return filtered_words[:6]

def post_links_saving(data):
    if os.path.exists("Post_Links.csv"):
        pass
    else:
        dataframe_1 = pd.DataFrame([{"Post_Link":""}])
        dataframe_1.to_csv("Post_Links.csv", index=False)
    field_names = ['Post_Link']
    with open('Post_Links.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        dictwriter_object.writerow(data)
        f_object.close()

def getting_all_data(url):
    df  = pd.read_csv("Post_Links.csv")
    already_present_links = list(df['Post_Link'])
    links = getting_video_links(url)
    for link in links:
        if link in already_present_links:
            continue
        data = {'Post_Link' : link}
        post_links_saving(data)
        result = requests.get(link)
        response = Selector(result)
        video = response.xpath("//video[@class='wp-video-shortcode']//a/@href").get()
        thumbnail = response.xpath('//div[@id="primary"]//img/@src').get()
        download(video)
        download(thumbnail)
        path = os.getcwd() + "\downloads"
        title = clean(response.css(".entry-title ::text").get())
        description = parse_description(response)
        tags = making_tags(title)
        time.sleep(2)
        video_path = glob.glob(f"{path}/*.mp4")
        # thumbnail_file_path = glob.glob(f"{path}/*.jpg")
        uploading_video(video_path[0],title[:95], description, tags)
        time.sleep(3)
        Remove_everything_from_folder()
        sleep_time = random.randint(60,7200)
        time.sleep(sleep_time)


if __name__=="__main__":
    # This is basically the first page links from wjoch this script is crawling and uploading videos of products.
    # I suggest you to mannually enter page links like page 2, page 3 etc if you want to go for pagination.
    url = "https://offerstore.top/page/1/"
    while True:
        getting_all_data(url)
        sleep_time = random.randint(60,7200)
        time.sleep(sleep_time)