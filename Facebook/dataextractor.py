from string import digits
import uuid
import logging
from string import digits
import json
import re
import html2text
import phonenumbers
from phonenumbers import Leniency
from utils import Utils
from exceptions import DataExtractionError, PhoneNumberExtractionError


class DataExtractor:
    
    def __init__(self, elements, output_folder):
        self._elements = elements
        self._output_folder = output_folder
        self._logger = logging.getLogger(__name__)

    def extract(self):
        return (self._filter_elements()
                    ._select_root_elements()
                    ._extract_data_from_elements())

    def _filter_elements(self):
        filtered_elements = []
        for element in self._elements:
            if len(element.get_attribute("innerHTML")) > 20 and " · " in element.get_attribute("innerHTML"):
                filtered_elements.append(element)

        self._elements = filtered_elements

        return self

    def _select_root_elements(self):
        root_elements = []
        for element in self._elements:
            root_element = element.find_element_by_xpath(
                ".//ancestor::div[@role='article']")
            root_elements.append(root_element)

        self._elements = root_elements

        return self

    def _extract_data_from_elements(self):
        data = []
        for element in self._elements:
            try:
                element_data = self._extract_element_data(element)

                try:
                    duplicate = next(duplicate
                                     for duplicate
                                     in data
                                     if duplicate["username"] == element_data["username"]
                                     and duplicate["title"] == element_data["title"])

                    self._logger.warning("New element {0} is a duplicate of {1}".format(
                        json.dumps(element_data, indent=4), json.dumps(duplicate, indent=4)))
                except StopIteration:
                    data.append(element_data)
            except DataExtractionError:
                pass

        return data

    def _extract_element_data(self, element):
        element_data = {}

        try:
            price_and_address_element = self._extract_price_and_address_element(
                element)
            images = self._extract_images(element)

            element_data["username"] = self._extract_username(element)
            element_data["title"] = self._extract_title(element)
            element_data["description"] = self._extract_description(element)
            element_data["price"] = self._extract_price(
                price_and_address_element)
            element_data["address"] = self._extract_address(
                price_and_address_element)
            element_data["phone"] = self._extract_phone_number(
                element_data["title"], element_data["description"])
            element_data["image1"] = images[0] if len(images) > 0 else ""
            element_data["image2"] = images[1] if len(images) > 1 else ""
            element_data["image3"] = images[2] if len(images) > 2 else ""
            element_data["image4"] = images[3] if len(images) > 3 else ""
            element_data["date"] = self._extract_date(element)
        except PhoneNumberExtractionError:
            self._logger.warning("Phone number extraction failed: {0}".format(
                json.dumps(element_data, indent=4)))
            raise DataExtractionError()
        except:
            self._logger.warning("Data extraction failed: {0}".format(
                json.dumps(element_data, indent=4)))
            raise DataExtractionError()

        return element_data

    def _extract_username(self, element):
        username_element = element.find_element_by_xpath(
            ".//descendant::a[@role='link']//descendant::span")

        return username_element.get_attribute("innerHTML")

    def _extract_title(self, element):
        title_element = element.find_element_by_xpath(
            ".//descendant::span[@dir='auto']//child::span//child::div[not(child::*) and not(contains(text(), 'Shared with'))]")

        return title_element.get_attribute("innerHTML")

    def _extract_description(self, element):
        description_element = element.find_element_by_xpath(
            ".//descendant::div[@data-ad-comet-preview='message']//descendant::span[@dir='auto']//child::div")
        description = html2text.html2text(
            description_element.get_attribute("innerHTML"))

        return " ".join(description.split())

    def _extract_price_and_address_element(self, element):
        return element.find_element_by_xpath(
            ".//descendant::span[@dir='auto']//child::span//child::span//child::div[not(contains(text(), 'Shared with'))]")

    def _extract_price(self, price_and_address_element):
        price = price_and_address_element.get_attribute(
            "innerHTML").split("<span>")[0]

        return "".join(c for c in price if c in digits)

    def _extract_address(self, price_and_address_element):
        return price_and_address_element.get_attribute("innerHTML").split("</span>")[-1]

    def _extract_phone_number(self, title, description):
        phone = ""
        textToSearch = title + " " + description
        for match in phonenumbers.PhoneNumberMatcher(textToSearch, "US", leniency=Leniency.POSSIBLE):
            phone = phonenumbers.format_number(
                match.number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            break

        # Custom phone regex (matches #446-3885)
        if len(phone) == 0:
            customPhones = re.findall(r"#[0-9]{3}-[0-9]{4}", textToSearch)
            if len(customPhones) > 0:
                phone = customPhones[0]
                phonenumbers.parse(phone, "US")
                phone = phonenumbers.format_number(
                    phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        if len(phone) == 0:
            raise PhoneNumberExtractionError()

        return self._format_phone_number(phone)

    def _extract_images(self, element):
        images = []
        image_elements = element.find_elements_by_xpath(
            ".//descendant::img")
        for _, image_element in enumerate(image_elements):
            image_src = image_element.get_attribute("src")

            if Utils.is_facebook_post_image(image_src):
                image_name = "{0}".format(uuid.uuid4().hex)+".jpg"
                Utils.download_image_as(
                    image_src, self._output_folder, image_name)
                images.append(image_name)

        return images

    def _extract_date(self, element):
        date_element = element.find_element_by_xpath(
            ".//descendant::span[@dir='auto']//child::span//child::span//child::span//child::a[@role='link']//child::span[not(child::*)]")
        date = date_element.get_attribute("innerHTML")

        return Utils.facebook_date_to_date(date).strftime("%B %d, %Y")

    def _format_phone_number(self, phone):
        digits_only = str("".join(c for c in phone if c in digits))
        national_number = digits_only[1:]

        if len(national_number) == 7:
            national_number = "876{0}".format(national_number)

        internation_number = "1{0}".format(national_number)

        phone = phonenumbers.parse(internation_number, "US")

        return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
