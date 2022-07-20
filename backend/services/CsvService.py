""" """
import logging

from models.Csv import Csv
from repositories.CsvRepository import CsvRepository
import utils.helper as helper


logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')


class CsvService(object):
    def __init__(self):
        self.model = Csv()
        self.repository = CsvRepository()


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

    def write_tracks(self, csv_file_path, tracks: list) -> None:
        # Check there is csv file
        if CsvService.is_not_csv(csv_file_path):
            helper.create_file(csv.file_path)

        # Check there is header
        if CsvService.is_not_header(csv_file_path):
            CsvRepository.add_columns(csv.file_path, csv.columns)

        self.repository.write(csv_file_path, self.model.columns, tracks)
        logger_con.info('Done to add tracks to CSV')
        return
    
    def show_track_info(self, track: list) -> None:
        logger_pro.info({
            'action': 'Show track info',
            'status': 'Run',
            'message': '',
        })
        for column, item in zip(self.csv_model.columns, track):
            print(f'\t{column}: {item}')
        
        logger_pro.info({
            'action': 'Show track info',
            'status': 'Success',
            'message': '',
        })
        return

    def retrieve_tracks(self, path: str) -> list:
        if CsvService.is_not_csv(path):
            return []

        if CsvService.is_not_header(path):
            return []

        tracks = []
        tracks_list = self.repository.read(path)

        logger_pro.info({
            'action': 'Retrieve tracks data from csv',
            'status': 'Run',
            'message': '',
            'data': {
                'path': path,
                'tracks_list': tracks_list
            }
        })

        for t in tracks_list:
            try:
                track = {
                    'name': t[0],
                    'artist': t[1],
                    'playlist_name': t[2],
                    'track_url': t[3],
                    'playlist_url': t[4],
                    'release_date': t[5],
                    'added_at': t[6],
                    'created_at': t[7],
                    'like': False
                }
                tracks.append(track)
                logger_pro.info({
                    'action': 'Retrieve tracks data from csv',
                    'status': 'Success',
                    'message': '',
                    'data': {
                        'track': track
                    }
                })
            except Exception as e:
                logger_pro.warning({
                    'action': 'Retrieve tracks data from csv',
                    'status': 'Fails',
                    'message': '',
                    'exception': e
                })
        return tracks
