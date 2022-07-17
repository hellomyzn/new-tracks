""" """
import logging

from models.Csv import Csv
from repositories.CsvRepository import CsvRepository
import utils.helper as helper


class CsvService(object):
    def __init__(self):
        self.logger_pro = logging.getLogger('production')
        self.logger_dev = logging.getLogger('develop')
        self.logger_con = logging.getLogger('console')
        self.csv_model = Csv()


    @classmethod
    def is_not_header(cls, path: str) -> bool:
        if not CsvRepository.get_header(path):
            return True
        else:
            return False

    @classmethod
    def is_not_csv(cls, path: str) -> bool:
        if not helper.is_file(path):
            return True
        else:
            return False

    @staticmethod
    def get_tracks(path: str) -> list:
        if CsvService.is_not_csv(path):
            return []

        if CsvService.is_not_header(path):
            return []

        data = CsvRepository.get_data(path)
        return data

    @staticmethod
    def get_track_by_name_and_artist(path: str,
                                     name: str,
                                     artist: str) -> list:
        if CsvService.is_not_csv(path):
            return []

        if CsvService.is_not_header(path):
            return []

        track = CsvRepository.get_first_data_by_name_and_artist(path,
                                                                name,
                                                                artist)
        return track

    @staticmethod
    def get_header_and_tracks(path: str) -> list:
        if CsvService.is_not_csv(path):
            return [], []

        if CsvService.is_not_header(path):
            return [], []

        header, data = CsvRepository.get_header_and_data(path)
        return header, data

    @staticmethod
    def add_tracks(csv, tracks: list) -> None:
        # Check there is csv file
        if CsvService.is_not_csv(csv.file_path):
            helper.create_file(csv.file_path)

        # Check there is header
        if CsvService.is_not_header(csv.file_path):
            CsvRepository.add_columns(csv.file_path, csv.columns)

        CsvRepository.add(csv.file_path, csv.columns, tracks)
        print('[INFO] - Done to add tracks to CSV')
        return
    
    def show_track_info(self, track: list) -> None:
        self.logger_pro.info({
            'action': 'Show track info',
            'status': 'Run',
            'message': '',
        })
        for column, item in zip(self.csv_model.columns, track):
            print(f'\t{column}: {item}')
        
        self.logger_pro.info({
            'action': 'Show track info',
            'status': 'Success',
            'message': '',
        })
        return
