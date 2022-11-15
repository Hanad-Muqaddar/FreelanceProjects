from time import sleep
from configparser import ConfigParser
from driverbuilder import DriverBuilder
from utils import Utils
from outputfile import OutputFile
from database import Database
from logging import Logging


class FacebookScraper:
    def __init__(self):
        Logging.setup()

    def execute(self):
        self._configparser = ConfigParser("config.ini").parse()
        self._output_folder = Utils.generate_output_folder_name()
        self._data = (DriverBuilder(self._configparser)
                      .passwordprompt()
                      .buildchrome()
                      .facebooklogin()
                      .sleep()
                      .visitgroup()
                      .scroll()
                      .create_output_folder(self._output_folder)
                      .extractdata())
        OutputFile(self._output_folder).save_data_to_file(self._data)
        Database(self._configparser).insert_data(self._data)
