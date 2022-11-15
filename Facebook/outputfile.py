import os
from more_itertools import unique_everseen
from csv import DictWriter


class OutputFile:
    def __init__(self, output_folder):
        self._output_folder = output_folder

    def save_data_to_file(self, data):
        output_name = os.path.join(self._output_folder, "output.csv")
        with open(output_name, "w", encoding="utf-8", newline="") as output_file:
            writer = DictWriter(output_file, ("username", "title", "description", "price",
                                              "address", "phone", "image1", "image2", "image3",
                                              "image4", "date"))
            writer.writeheader()
            writer.writerows(data)
