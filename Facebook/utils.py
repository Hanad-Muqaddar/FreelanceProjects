import os
import urllib.request
import datetime
from PIL import ImageFile
import requests


class Utils:
    @staticmethod
    def get_image_size(url):
        file = urllib.request.urlopen(url)

        size = (0, 0)
        p = ImageFile.Parser()
        while True:
            data = file.read(1024)

            if not data:
                break

            p.feed(data)
            if p.image:
                size = p.image.size
                break

        file.close()

        return size

    @staticmethod
    def is_facebook_post_image(image_src):
        image_size = Utils.get_image_size(image_src)

        if image_size[0] > 100 and image_size[1] > 100:
            return True
        else:
            return False

    @staticmethod
    def download_image_as(image_src, folder, filename):
        image_data = requests.get(image_src).content
        full_filename = os.path.join(folder, filename)
        with open(full_filename, "wb") as handler:
            handler.write(image_data)

    @staticmethod
    def facebook_date_to_date(facebook_date):
        if "hr" in facebook_date or "hrs" in facebook_date:
            return Utils._facebook_date_today_hours(facebook_date)
        elif "min" in facebook_date or "mins" in facebook_date:
            return Utils._facebook_date_today_minutes(facebook_date)
        elif "Yesterday" in facebook_date:
            return Utils._facebook_date_yesterday(facebook_date)
        else:
            return Utils._facebook_date_old(facebook_date)

    @staticmethod
    def _facebook_date_today_hours(facebook_date):
        hours = int(facebook_date.split()[0])

        return datetime.datetime.now() - datetime.timedelta(hours=hours)

    @staticmethod
    def _facebook_date_today_minutes(facebook_date):
        minutes = int(facebook_date.split()[0])

        return datetime.datetime.now() - datetime.timedelta(minutes=minutes)

    @staticmethod
    def _facebook_date_yesterday(facebook_date):
        return datetime.datetime.now() - datetime.timedelta(1)

    @staticmethod
    def _facebook_date_old(facebook_date):
        month_name = facebook_date.split()[0]
        day_number = int(facebook_date.split()[1])

        month_number = datetime.datetime.strptime(month_name, "%B").month

        return datetime.datetime.now().replace(month=month_number, day=day_number)

    @staticmethod
    def generate_output_folder_name():
        current_time = datetime.datetime.now().strftime('%Y%m%dT%H%M%S%f%z')

        return "%s-output" % current_time
