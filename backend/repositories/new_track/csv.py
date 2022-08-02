import csv
import logging

from models.new_track import NewTrackModel
from repositories.new_track.interfaces.new_track_repository import NewTrackRepoInterface
import utils.helper as helper
import utils.setting as setting

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')

class CsvNewTrackRepository(NewTrackRepoInterface):
    """
    A class used to represent a CSV repository

    Attributes
    ----------
    model:
        A csv model
    path: str
        A path of csv to manage tracks set up on model
    columns: list
        Columns set up on model
    Methods
    ------
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        self.model = NewTrackModel()
        self.columns = self.model.get_columns()
        if setting.ENV == 'dev':
            self.path = setting.FILE_PATH_OF_CSV_TEST
        else:
            self.path = setting.FILE_PATH_OF_CSV
        print(self.path)

    def all(self) -> list:
        """ 
            Read all tracks
            
            Parameters
            ----------
            None

            Raises
            ------
            Warning
                if there is no file or you set path up wrongly.
                if there is no any track data in csv file.
            Exception
                If it fails to read tracks

            Return
            ------
            tracks: list
                A list of tracks (each tracks was not dict, just a list)
        """

        logger_pro.info({
            'action': 'Read all tracks from csv',
            'status': 'Run',
            'message': '',
            'data': {
                'path': self.path
            }
        })

        tracks = []
        if not helper.exists_file(self.path):
            return tracks

        if not self.read_header():
            return tracks

        try:
            with open(self.path, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row in csv_reader:
                    track = {}

                    for r, c in zip(row, self.columns):
                        track[c] = r
                    tracks.append(track)

            logger_pro.info({
                'action': 'Read all tracks from csv',
                'status': 'Success',
                'message': '',
                'data': {
                    'tracks_len': len(tracks)
                }
            })
        except Exception as e:          
            logger_pro.warning({
                'action': 'Read all tracks from csv',
                'status': 'Fails',
                'message': '',
                'exception': e,
                'data': {
                    'path': self.path
                }
            })
        return tracks

    def add(self, data: dict) -> None:
        self.write(data)
        return None

    def read_header(self) -> list:
        """ Read header data on CSV

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
            The header on the path of CSV
        """

        logger_pro.debug({
            'action': 'Read header data from csv',
            'status': 'Run',
            'message': '',
            'data': {
                'path': self.path
            }
        })

        try:
            with open(self.path, 'r', newline='') as csvfile:
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
                    'path': self.path
                }
            })
        if header is None:
            logger_pro.warning({
                'action': 'Read header data from csv',
                'status': 'Fails',
                'message': 'There is no header on the CSV',
                'data': {
                    'path': self.path
                }
            })
            
        return header

    def write_header(self) -> None:
        """ Write header on CSV.

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
                'path': self.path,
                'columns': self.columns
            }
        })
        try:
            with open(self.path, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.columns)
                writer.writeheader()

            logger_pro.warning(f'Add header on csv ({self.path})')
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


    def write(self, track: dict) -> None:
        """ Write tracks on CSV.

        If there is no csv file to write,
        create a csv file.

        If there is no header on csv,
        Add headers on csv.

        Parameters
        ----------
        track: dict
            A track dict to be written on CSV.

        Raises
        ------
        Exception
            If it fails to write on CSV

        Return
        ------
        None
        """
        # Check there is csv file
        if not helper.exists_file(self.path):
            helper.create_file(self.path)

        # Check there is header
        if self.read_header() is None:
            self.write_header()
    
        logger_pro.info({
            'action': 'Write a track data on CSV',
            'status': 'Run',
            'message': '',
            'data': {
                'path': self.path
            }
        })
        try:
            with open(self.path, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.columns)
                writer.writerow(track)
                logger_pro.info({
                    'action': 'Write a tarack data on CSV',
                    'status': 'Success',
                    'message': '',
                    'track': track
                })
        except Exception as e:
            logger_pro.error({
                'action': 'Write a track data on CSV',
                'status': 'Fails',
                'message': '',
                'exception': e
            })
        return

    def find_track_first(self, track: dict) -> list:
        """ find the first track by name and artist on CSV

        Parameters
        ----------
        track: dict
            A track dict to find

        Raises
        ------
        Exception
            If it fails to find it

        Return
        ------
        track_from_csv: list
            the first track found on CSV
        """
        track_from_csv = []
        if not helper.exists_file(self.path):
            return track_from_csv

        if not self.read_header():
            return track_from_csv

        with open(self.path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                if row[0] == track['name'] and row[1] == track['artist']:
                    track_from_csv = row
                    return track_from_csv

    def find_by_name_and_artist(self, name: str, artist: str) -> dict:
        pass
    
    def delete_by_name_and_artist(self, name: str, artist: str) -> None:
        pass