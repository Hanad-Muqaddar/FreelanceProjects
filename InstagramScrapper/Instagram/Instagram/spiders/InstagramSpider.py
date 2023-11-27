from scrapy.crawler import CrawlerProcess
import scrapy
import json
import time
import os


class InstagramspiderSpider(scrapy.Spider):
    name = 'InstagramSpider'

    def start_requests(self):
        headers = {
                    'authority': 'www.instagram.com',
                    'method': 'GET',
                    'scheme': 'https',
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'cookie': 'csrftoken=ps9ENLEa0uq5XJYjEzbzPGNFTUMi4I1t; ig_did=98987A3F-DBAD-403D-9314-D7294E4369F0; ig_nrcb=1; mid=Y0ek-gALAAFcHLjaovAhCIZEIUFC; datr=tJZjYyyoCf3yrX7yhugoDxt1; dpr=1.25; fbm_124024574287414=base_domain=.instagram.com; fbsr_124024574287414=CoXzxJbvpPjMrfN6cq6hng9JbTAt1ddLRwESFOgnY9o.eyJ1c2VyX2lkIjoiMTAwMDg3MTA1MTM1NTUzIiwiY29kZSI6IkFRQmpXeXZLRXVuekNkNjBuZGctM3ZlMW5jNjFULTg1ZEZ0TmJsYVl6dm1zTlBjY0JIS3ZDY1Awc3RmVml6aTdiOGlpM2hnSnBzWFRWSDdIVkVJRzJqd3F3SkFHR0ZrU2I3M1pLTlZBeHFUN09jNUV0ck1HLU1HQkU0eW02Ym5ldnAtSFh3SmlCYmI4ODQ4ZUxwdC1KakJLWnJHQmtTcHBSaXNqUzA3cnFNTlJNZ2psQ2VNWFI3R3BGMkJfcnZid1NaT1RVRUVFQmRNV1V3d0I1YXJKdGRaNWtMZG1IRXdUYTlaNVRMRWg1N0hBb2lmX2FxT1FDa0FHSk56dlZ0WlBKZXZoWGtaWDBFd3FmRlJYY2l3ZnFPa2hITk9SVlg2S1dsSEI0TzByakhUMEkxNDhpRW5VcExfZ0pPc0MwamhWbkhjR0ZQR3EtWnZQcWNPc1djd0tvdlI4Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUs4ZlpCUFpBSmRvbW0yR3MwSlpDdWh2cWg0Q3ZLWkEyWkJiMDFwaWNjWkF5MnM1STA0ZVlhaDVlRFVzMGEyeGZ1bUNhTGs3bG5HOHBvMlpCRGlPdThGT2U2cXJ0ekloYnNLcVJOTDd0UWNCYTI1aDJrOGFDelZFUHM2QlRKZWN5WkFsNXd4aWlscWNGUzVjYzlFV1JhWkJ0eEVVbGhyWkJaQmE4TEtaQ3pOSlpDUVVZTHMzMWJQVHl4alFaRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNjY3NjQzMjQ4fQ; fbsr_124024574287414=u1KMk9zU1iGs0CraNwSIW1ax4n9GpoFvvJ7ihADlTx8.eyJ1c2VyX2lkIjoiMTAwMDg3MTA1MTM1NTUzIiwiY29kZSI6IkFRQW5vZkw5b180ZTJnNzVNVUVxc3pPQU5RS0dDZVUwMTBpRmFVQ1ZiRS13dC1FVjdsdWNGZzU4YWJVVy1UUmtySWZ5MVJ6dTFiSTN0U1Y2M3ZoRmF3ZUhvQ1RoTVlwRlVKZ25sVnRkeDdhMkE3Nm5sNWVPTlJzTDJpQ1JNOHFjcnRCNGV5TkdBMUpTWldRZHV4LVctRVd2LTZCRXBzYzJmY3BlU3NEa2RXTVU2TDhIYkdwd3lESjl4QWQtaEhGUE1nVF9QTVFFMmFBVUpjNmxiM011aEsxV1ZaTE5iNkFmdEJHQWZaaDRZNnBWQ3QtLVIwQkUzdnEwakRra1AzaEpSTTIxQldBUGVuN3pYQ0tFeHhRMjdiZnVwMWlvMUIwY256MzdYMzJIdnM2cnViQUEyS2hZM2ZrSjRWMFFBaWVqcU15U0VRR3pIbXhnMElSRV9VMHllYlUxIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUhLazJ2ZGtscllhM1VtazA2QjRzbjE1ek16d0xhelBDNUVsQ0ZSQ2xkZW1Uejd1NGxzUEFFMnBRTUdEcnJ0TGJJYlpCUjNMREw3WkFYTmwxWVpCN3pzV0J2TW1ScktaQVRJc3V4YW5iWkJWSlpDMGxtRmpSM01FUFk0bG5hRjNXam5relJ2RTFBTWJ3c1pBR2daQ3R4QlpDNXJNSlpCVVdxM0JCdHNuSWVZWEhPakxWS0ZFUEZKZnNaRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNjY3NjQzMjE3fQ; csrftoken=mYockGR2TkmPxoXEy3L0lrWK3XCg0Vjr; ig_did=9B7CD393-B997-487B-A11E-45C2A1E3F49B; ig_nrcb=1; mid=Y2ZAkgAEAAG-vizk73sx8ZlDrePN',
                    'pragma': 'no-cache',
                    'sec-ch-prefers-color-scheme': 'light',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                    'viewport-width': '1536',
                    'x-csrftoken': 'ps9ENLEa0uq5XJYjEzbzPGNFTUMi4I1t',
                    'x-ig-app-id': '936619743392459'
                }
        usernames = ['adidas']
        for username in usernames:
            url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)
    
    def parse(self, response):
        data = json.loads(response.body)
        item = {}
        item['Username'] = data['data']['user']['full_name']
        item['Total_Posts'] = data['data']['user']['edge_owner_to_timeline_media']['count']
        item['Total Videos'] = data['data']['user']['edge_felix_video_timeline']['count']
        item['Followers'] = data['data']['user']['edge_followed_by']['count']
        item['Following'] = data['data']['user']['edge_follow']['count']
        item['HashTags'] = self.parse_hash_tags(response)
        if data['data']['user']['is_business_account']:
            item['Business or Personal'] = "Business"
        else:
            item['Business or Personal'] = "Personal"
        item['Profesional_Account'] = data['data']['user']['is_professional_account']
        item['Phone_Number'] = data['data']['user']['business_phone_number']
        item['Business_Category'] = data['data']['user']['business_category_name']
        item['Profile_Picture'] = data['data']['user']['profile_pic_url_hd']
        item['Videos_Data'] = self.parse_videos_data(response)
        item['Images'] = self.parse_images_data(response)
        yield item
    
        
    def parse_hash_tags(self, response):
        data = json.loads(response.body)
        hash_tags_data = data['data']['user']['biography_with_entities']['entities']
        hashtags = []
        for tag in hash_tags_data:
            hashtags.append(tag['hashtag']['name'])
        return hashtags

    
    def parse_videos_data(self, response):
        data = json.loads(response.body)
        data_lists = ['edge_felix_video_timeline','edge_owner_to_timeline_media']
        videos_list = []
        for dat in data_lists:
            videos_data = data['data']['user'][dat]['edges']
            for vid in videos_data:
                if vid['node']['is_video']:
                    it = {}
                    try:
                        it['video_url'] = vid['node']['video_url']
                    except:
                        it['video_url'] = ""
                    try:
                        it['Post_Url'] = "https://www.instagram.com/p/" + vid['node']['shortcode'] + "/"
                    except:
                        it['Post_Url'] = ""
                    try:
                        it['video_views_count'] = vid['node']['video_view_count']
                    except:
                        it['video_views_count'] = ""
                    try:
                        it['video_comment_count'] = vid['node']['edge_media_to_comment']['count']
                    except:
                        it['video_comment_count'] = ""
                    try:
                        it['video_likes'] = vid['node']['edge_liked_by']['count']
                    except:
                        it['video_likes'] = ""
                    try:
                        it['video_duration'] = vid['node']['video_duration']
                    except:
                        it['video_duration'] = ""
                    videos_list.append(it)
        return videos_list
    
    def parse_images_data(self, response):
        data = json.loads(response.body)
        data_lists = ['edge_felix_video_timeline','edge_owner_to_timeline_media']
        images_list = []
        for dat in data_lists:
            images_data = data['data']['user'][dat]['edges']
            for img in images_data:
                if img['node']['is_video']:
                    continue
                else:
                    images_container = img['node']['edge_sidecar_to_children']['edges']
                    for image in images_container:
                        im = {}
                        im['Image_Url'] = image['node']['display_url']
                        im['PostUrl'] = "https://www.instagram.com/p/"+image['node']['shortcode'] + "/"
                        images_list.append(im)
        return images_list

def return_json_object():
    path = "D:/DestopFolder/Five_Proj/InstagramScrapper/Instagram"
    with open(f'{path}/Insta.json') as f:
        data = json.load(f)
    os.remove(f'{path}/Insta.json')
    return data
    
if __name__ == '__main__':

    process = CrawlerProcess(settings={
        "FEEDS": {
            "Insta.json": {"format": "json"},
        },
    })
    process.crawl(InstagramspiderSpider)
    process.start()
    time.sleep(3)
    josn_data = return_json_object()
    print(josn_data)
