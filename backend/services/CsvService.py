""" """
import logging

from models.Csv import Csv
from models.tests.csv import TestCsvModel
from repositories.CsvRepository import CsvRepository
import utils.helper as helper
import utils.setting as setting


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
        # self.model = Csv()
        self.model = TestCsvModel()
        self.repository = CsvRepository(self.model)
    
    @classmethod
    def convert_csv_into_tracks_dict(cls, csv: list) -> list:
        """ Convert csv list (without keys) into tracks dict

        Parameters
        ----------
        csv: list
            A csv tracks to be converted into tracks dict
        
        Raises
        ------
        Warning

        Return
        ------
        converted_tracks: list
            A tracks dict data
        """

        converted_tracks = []
        logger_pro.info({
            'action': 'Convert csv list into tracks dict',
            'status': 'Run',
            'message': '',
            'args': {
                'csv': csv
            }
        })
        for c in csv:
            try:
                track_dict = {
                    'name': c[0],
                    'artist': c[1],
                    'playlist_name': c[2],
                    'track_url': c[3],
                    'playlist_url': c[4],
                    'release_date': c[5],
                    'added_at': c[6],
                    'created_at': c[7],
                    'like': c[8]
                }
                converted_tracks.append(track_dict)
                logger_pro.info({
                    'action': 'Convert csv list into tracks dict',
                    'status': 'Success',
                    'message': '',
                    'data': {
                        'track': track_dict
                    }
                })
            except Exception as e:
                logger_pro.error({
                    'action': 'Convert csv list into tracks dict',
                    'status': 'Fails',
                    'message': '',
                    'exception': e,
                    'data': {
                        'track': c
                    }
                })
        return converted_tracks

    def retrieve_new_tracks(self, tracks: list) -> list:
        """ Retrieve new tracks by comparing to tracks on csv file.
        
        Parameters
        ----------
        tracks: list
            A tracks data

        Raises
        ------
        Exception
            It fails to retreive new tracks

        Return
        ------
        new_tracks: list
            A new tracks list from tracks data which doesn't exist 
            in the tracks_from_csv
                
        """
        new_tracks = []
        tracks_from_csv = self.read_tracks_all()
        
        logger_pro.info({
            'action': 'Retrieve new tracks by comparing to tracks on csv file.',
            'status': 'Run',
            'message': '',
            'args': {
                'tracks': tracks,
                'tracks_from_csv': tracks_from_csv
            }
        })

        # If there is no track data, it regards all tracks as new tracks
        if not tracks_from_csv:
            logger_con.info(f'The number of new tracks is {len(tracks)}')
            logger_pro.warning({
                'action': 'Retrieve new tracks by comparing to tracks on csv file.',
                'status': 'Warning',
                'message': 'There is no tracks data in on csv ',
                'args': {
                    'tracks': tracks,
                    'tracks_from_csv': tracks_from_csv
                }
            })

            return tracks
        
        # Prepare a list from retrieved tracks to check which tracks are new for this time
        converted_tracks = self.convert_tracks_into_name_and_artist(tracks)

        # Prepare a list from csv to check which tracks are new for this time
        converted_csv_tracks = self.convert_tracks_into_name_and_artist(tracks_from_csv)    

        # Check which tracks are new
        for i, track in enumerate(converted_tracks):
            if track in converted_csv_tracks:
                continue
            new_tracks.append(tracks[i])

        logger_con.info(f'The number of new tracks is {len(new_tracks)}')
        logger_pro.info({
            'action': 'Retrieve new tracks by comparing to tracks on csv file.',
            'status': 'Success',
            'message': '',
            'data': {
                'track': new_tracks
            }
        })

        return new_tracks

    def read_tracks_all(self) -> list:
        """ Read all tracks data and convert csv data to dict from CSV.
        
        If there is no file or there is no any track data,
        return a empty list.

        Parameters
        ----------
        None
        
        Raises
        ------
        None

        Return
        ------
        tracks: list
            A tracks data list read on CSV.
        """

        tracks = []
        tracks_csv = self.repository.read_all()

        tracks = CsvService.convert_csv_into_tracks_dict(tracks_csv)

        return tracks

    def convert_tracks_into_name_and_artist(self, tracks: list) -> list:
        """ Convert tracks into name and artist

        Parameters
        ----------
        tracks: list
            A tracks list to be converted into a list 
            containing dict which key sare name and artist

        Raises
        ------
        Exception
            If it fails to convert them

        Return
        ------
        converted_tracks: list
            A tracks list converted into a list 
            containing dict which keys are name and artist
        """
        converted_tracks = []
        logger_pro.info({
            'action': 'Convert tracks into name and artist',
            'status': 'Run',
            'message': '',
            'args': {
                'length': len(tracks),
                'tracks': tracks
            }
        })
        try:
            converted_tracks = [{'name': t['name'], 'artist': t['artist']} for t in tracks]
            logger_pro.info({
                'action': 'Convert tracks into name and artist',
                'status': 'Success',
                'message': '',
                'data': {
                    'length': len(converted_tracks),
                    'converted_tracks': converted_tracks
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Retrieve tracks from playlists',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'length': len(tracks),
                    'tracks': tracks
                }
            })
        return converted_tracks

    def write_tracks(self, tracks: list) -> None:
        """ Write tracks on CSV.

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
        if not tracks:
            logger_con.info('There is no new tracks to add to CSV this time.')
            logger_pro.info('There is no new tracks to add to CSV this time.')

        self.repository.write(tracks)
        return



    @staticmethod
    def get_track_by_name_and_artist(path: str,
                                     name: str,
                                     artist: str) -> list:
        if not helper.exists_file(path):
            return []
        if not self.repository.read_header(path):
            return []

        track = CsvRepository.get_first_data_by_name_and_artist(path,
                                                                name,
                                                                artist)
        return track
    
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