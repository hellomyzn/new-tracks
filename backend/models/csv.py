import csv

from interfaces.table import Table

class CSV(Table):
    def __init__(self):
        self.columns = CSV.get_columns()

    @classmethod
    def create_columns(cls, url, columns):
        print('Create header on CSV')
        with open(url, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()

    @classmethod
    def is_not_columns(cls, url):
        with open(url, 'r', newline='') as csvfile:
            data = csvfile.readline()
            if not data:
                return True
            else:
                return False

    def write(self, tracks, url):
        if CSV.is_not_columns(url):
            CSV.create_columns(url, self.columns)

        with open(url, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            for track in tracks:
                writer.writerow(track)
                print(f"[WRITING]: {track}")