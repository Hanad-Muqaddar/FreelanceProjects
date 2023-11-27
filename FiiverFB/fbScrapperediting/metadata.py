from scrapy import Selector
import time
from login_form import driver_return


def extracting_comments(response):
    a = [1,2,3,4,5,6,7,8,9]
    b = [1,2,3]
    for j in b:
        for i in a:
            # print(i, j)
            number_of_comments = response.xpath(f'normalize-space(((//div[@data-pagelet="TahoeRightRail"]//span[@aria-label="See who reacted to this"]/parent::div/parent::div//div)[{i}]//span)[{j}])').get()
            if number_of_comments == "" or number_of_comments == None:
                continue
            elif "comments" in number_of_comments.lower():
                return number_of_comments
    number_of_comments = ""
    return number_of_comments

def extracting_views(response):
    a = [1,2,3,4,5,6,7,8,9]
    b = [1,2,3]
    for j in b:
        for i in a:
            # print(i, j)
            number_of_views = response.xpath(f'normalize-space(((//div[@data-pagelet="TahoeRightRail"]//span[@aria-label="See who reacted to this"]/parent::div/parent::div//div)[{i}]//span)[{j}])').get()
            if number_of_views == "" or number_of_views == None:
                continue
            elif "views" in number_of_views.lower():
                return number_of_views
    number_of_views = ""
    return number_of_views

def get_facebook_video_post_data(url):
    driver = driver_return()
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)
    response = Selector(text = driver.page_source.encode('utf-8'))
    time.sleep(3)
    number_of_likes = response.xpath('(//div[@data-pagelet="TahoeRightRail"]//span[@aria-label="See who reacted to this"]/parent::div//span)[12]/text()').get()
    number_of_comments = extracting_comments(response)
    number_of_views = extracting_views(response)
    video_post_date = response.xpath('(//div[@role="complementary"]//a[@aria-label != "a link to a video"])[2]/@aria-label').get()
    video_title = response.xpath('normalize-space(((//div[@role="complementary"]//div[@data-pagelet="TahoeRightRail"]/div/div)[1]/div)[3]//div[@dir="auto"])').get()
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
    data = {'Post_Link' : url, "Likes":number_of_likes, "Comments":number_of_comments, "Views" : number_of_views, "Video_Title": video_title, "Date": video_post_date}
    return data


url = "https://web.facebook.com/JacobReesMogg/videos/234910231990171/"
data = get_facebook_video_post_data(url)
print("********************************")
print("********************************")
print(data['Post_Link'])
print(data['Likes'])
print(data['Comments'])
print(data['Views'])
print(data['Video_Title'])
print(data['Date'])
print("********************************")
print("********************************")


    



