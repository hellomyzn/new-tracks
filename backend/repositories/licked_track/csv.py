import csv
from configparser import ConfigParser
import logging

from models.new_track import NewTrackModel
import utils.helper as helper
import utils.setting as setting

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')
CONFIG_FILE = './config/config.ini'
CONFIG = ConfigParser()
CONFIG.read(CONFIG_FILE)


class CsvLikedTrackRepository():

    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        self.header = ["name", "artist", "url", "release_date", "added_at", "created_at"]

        if setting.ENV == 'dev':
            self.path = setting.FILE_PATH_OF_CSV_TEST
        else:
            self.path = CONFIG["CSV"]["DIR"] + CONFIG["CSV"]["LIKED_TRACKS"]

    def get_all(self) -> list:
        tracks = []

        # If there is no csv file, return empty list
        if not helper.exists_file(self.path):
            return tracks

        # If there is no header on csv file, return empty list
        header = CsvLikedTrackRepository.read_header(self.path)
        if not header:
            return tracks

        try:
            with open(self.path, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row in csv_reader:
                    track = {}

                    # Set track dict
                    for r, h in zip(row, header):
                        track[h] = r

                    tracks.append(track)
            if tracks:
                logger_pro.info({
                    'action': 'Read all tracks from csv',
                    'status': 'Success',
                    'message': '',
                    'data': {
                        'tracks_len': len(tracks)
                    }
                })
            else:
                logger_pro.warning({
                    'action': 'Read all tracks from csv',
                    'status': 'Warning',
                    'message': 'There is no track on CSV'
                })

        except Exception as e:
            logger_pro.error({
                'action': 'Read all tracks from csv',
                'status': 'Fails',
                'message': '',
                'exception': e,
                'data': {
                    'path': self.path
                }
            })

        return tracks

    def add_tracks(self, tracks: list) -> None:
        # If there is no csv file, return empty list
        if not helper.exists_file(self.path):
            return None

        # If there is no header on csv file, return empty list
        header = CsvLikedTrackRepository.read_header(self.path)
        if not header:
            CsvLikedTrackRepository.write_header(self.path, self.header)
            header = self.header

        try:
            with open(self.path, 'a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=header)
                writer.writerows(tracks)

        except Exception as e:
            print(e)
        return

        return None

    def add_track(self, track: list) -> None:
        # If there is no csv file, return empty list
        if not helper.exists_file(self.path):
            return None

        # If there is no header on csv file, return empty list
        header = CsvLikedTrackRepository.read_header(self.path)
        if not header:
            CsvLikedTrackRepository.write_header(self.path, self.header)
            header = self.header

        try:

            with open(self.path, 'a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=header)
                writer.writerow(track)

        except Exception as e:
            print(e)

        return None

    @classmethod
    def read_header(cls, path) -> list:
        """
            Read header data on CSV.

            Parameters
            ----------
            None

            Raises
            ------
            Exception
                If you fail to read the header.

            Return
            ------
            header: str
                The header on the path of CSV.
        """

        logger_pro.debug({
            'action': 'Read header data from csv',
            'status': 'Run',
            'message': ''
        })

        header = []
        try:
            with open(path, 'r', newline='') as csvfile:
                csv_dict_reader = csv.DictReader(csvfile)
                header = csv_dict_reader.fieldnames

            logger_pro.debug({
                'action': 'Read header data from csv',
                'status': 'Success',
                'message': '',
                'data': {
                    'header': header
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Read header data from csv',
                'status': 'Fails',
                'message': '',
                'exception': e,
                'data': {
                    'path': path
                }
            })
        if header is None:
            logger_pro.warning({
                'action': 'Read header data from csv',
                'status': 'Warning',
                'message': 'There is no header on the CSV',
                'data': {
                    'path': path
                }
            })

        return header

    @classmethod
    def write_header(cls, path: str, header: list) -> None:
        """
            Write header on CSV.

            Parameters
            ----------
            tracks: list
                A tracks list to be written on CSV.

            Raises
            ------
            Exception
                If it fails to write on CSV

            Return
            ------
            None
        """
        logger_pro.info({
            'action': 'Write header on CSV.',
            'status': 'Run',
            'message': '',
            'data': {
                'path': path,
                'header': header
            }
        })
        try:
            with open(path, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()

            logger_pro.warning(f'Add header on csv ({path})')
            logger_pro.info({
                'action': 'Write header on CSV.',
                'status': 'Success',
                'message': '',
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Write header on CSV.',
                'status': 'Fails',
                'message': '',
                'exception': e
            })

        return

    def write_dict(self, track: dict) -> None:
        pass

    def find_by_url(self, url: str) -> None:
        pass

    def delete_by_url(self, url: str) -> None:
        pass
