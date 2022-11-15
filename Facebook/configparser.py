import configparser


class ConfigParser:
    def __init__(self, filename):
        self._config = configparser.ConfigParser()
        self._config.read(filename)

    def parse(self):
        self.waiting_time = self._config.getint("REQUIRED", "WAITING_TIME")
        self.driver_path = self._config.get("REQUIRED", "DRIVER_PATH")
        self.group_name = self._config.get("REQUIRED", "GROUP_NAME")
        self.facebook_login = self._config.get("REQUIRED", "FACEBOOK_LOGIN")
        self.number_of_scrolls = self._config.getint(
            "REQUIRED", "NUMBER_OF_SCROLLS")
        self.scroll_timeout = self._config.getint("REQUIRED", "SCROLL_TIMEOUT")
        self.request_timeout = self._config.getint(
            "REQUIRED", "REQUEST_TIMEOUT")
        self.headless_chrome = self._config.getboolean(
            "REQUIRED", "HEADLESS_CHROME")
        self.database_host = self._config.get("REQUIRED", "DATABASE_HOST")
        self.database_username = self._config.get(
            "REQUIRED", "DATABASE_USERNAME")
        self.database_password = self._config.get(
            "REQUIRED", "DATABASE_PASSWORD")
        self.database_name = self._config.get("REQUIRED", "DATABASE_NAME")

        return self

    def parse_categories(self):
        self.auto_keywords = self._config.get(
            "CATEGORIES", "AUTO").split(",")
        self.jobs_keywords = self._config.get(
            "CATEGORIES", "JOBS").split(",")
        self.services_keywords = self._config.get(
            "CATEGORIES", "SERVICES").split(",")
        self.electronics_keywords = self._config.get(
            "CATEGORIES", "ELECTRONICS").split(",")
        self.realestate_keywords = self._config.get(
            "CATEGORIES", "REALESTATE").split(",")

        return self
