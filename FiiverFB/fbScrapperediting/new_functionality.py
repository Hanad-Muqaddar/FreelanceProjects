from scrapy import Selector
import time
from csv import DictWriter
import pandas as pd
import os
from login_form import driver_return


def post_data_saving(data):
    if os.path.exists("Posts_Data.csv"):
        pass
    else:
        dataframe_1 = pd.DataFrame([{"Post_Link":"", "Likes":"", "Comments":"", "Views":"","Video_Title": "", "Date":"", "Download_Url":""}])
        dataframe_1.to_csv("Posts_Data.csv", index=False)
    field_names = ['Post_Link', 'Likes', 'Comments', 'Views', 'Video_Title','Date', 'Download_Url']
    with open('Posts_Data.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        dictwriter_object.writerow(data)
        f_object.close()


def get_facebook_video_post_data(url):
    driver = driver_return()
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)
    response = Selector(text = driver.page_source.encode('utf-8'))
    time.sleep(3)
    number_of_likes = response.xpath('(//div[@data-pagelet="TahoeRightRail"]//span[@aria-label="See who reacted to this"]/parent::div//span)[12]/text()').get()
    number_of_comments = response.xpath('normalize-space(((//div[@data-pagelet="TahoeRightRail"]//span[@aria-label="See who reacted to this"]/parent::div/parent::div//div)[7]//span)[2])').get()
    number_of_views = response.xpath('normalize-space(((//div[@data-pagelet="TahoeRightRail"]//span[@aria-label="See who reacted to this"]/parent::div/parent::div//div)[9]//span)[3])').get()
    video_post_date = response.xpath('(//div[@role="complementary"]//a[@aria-label != "a link to a video"])[2]/@aria-label').get()
    video_title = response.xpath('((//div[@role="complementary"]//div[@data-pagelet="TahoeRightRail"]/div/div)[1]/div)[3]//div[@dir="auto"]/text()').get()
    if "comment" in number_of_comments.lower():
        pass
    elif "comment" in number_of_views.lower():
        number_of_comments = number_of_views
        number_of_views = ""
    elif "views" in number_of_comments.lower():
        number_of_views = number_of_comments
        number_of_comments = ""
    elif "views" in number_of_views.lower():
        pass
    return number_of_likes, number_of_comments, number_of_views, video_post_date, url, video_title



likes, comments, views, date, post_link, title = get_facebook_video_post_data(url)
data = {'Post_Link' : post_link, "Likes":likes, "Comments":comments, "Views" : views, "Video_Title": title, "Date": date, 'Download_Url':src}
post_data_saving(data)