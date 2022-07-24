""" """
import logging

from models.Csv import Csv
from repositories.CsvRepository import CsvRepository
import utils.helper as helper


logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')


class CsvService(object):
    """
    A class used to represent a CSV service

    Attributes
    ----------
    model:
        A csv model
    repository:
        A csv repository

    Methods
    ------
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        self.model = Csv()
        self.repository = CsvRepository()

    def is_not_header(self, path: str) -> bool:
        """

        """
        if not self.repository.read_header(path):
            return True
        else:
            return False

    @staticmethod
    def get_track_by_name_and_artist(path: str,
                                     name: str,
                                     artist: str) -> list:
        if not helper.is_file(path):
            return []
        if not self.repository.read_header(path):
            return []

        track = CsvRepository.get_first_data_by_name_and_artist(path,
                                                                name,
                                                                artist)
        return track

    def write_tracks(self, csv_file_path, tracks: list) -> None:
        # Check there is csv file
        if not helper.is_file(csv_file_path):
            helper.create_file(csv.file_path)

        # Check there is header
        if self.is_not_header(csv_file_path):
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

    def read_tracks(self, path: str) -> list:
        """ Read tracks data from CSV.
        
        If there is no file or there is no any track data,
        return a empty list.

        Parameters
        ----------
        path: str
            A path of csv.
        
        Raises
        ------
        Warning
            if there is no file or you set path up wrongly.
            if there is no any track data in csv file.

        Return
        ------
        tracks: list
            A tracks data list read on CSV.
        """

        if not helper.is_file(path):
            return []

        if not self.repository.read_header(path):
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
                    'like': t[8]
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
                logger_pro.error({
                    'action': 'Retrieve tracks data from csv',
                    'status': 'Fails',
                    'message': '',
                    'exception': e,
                    'data': {
                        'track': t
                    }
                })
        return tracks
