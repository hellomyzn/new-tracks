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
        self.model = Csv()
        # self.model = TestCsvModel()
        self.repository = CsvRepository(self.model)

    def convert_csv_into_track_dict(self, csv: list) -> list:
        """ Convert one track of csv list (without keys) into track dict

        Parameters
        ----------
        csv: list
            A csv track to be converted into track dict
        
        Raises
        ------
        Warning

        Return
        ------
        converted_tracks: list
            A track dict data
        """

        converted_track = {}
        logger_pro.info({
            'action': 'Convert csv list into track dict',
            'status': 'Run',
            'message': '',
            'args': {
                'csv': csv
            }
        })
        try:
            for i, v in enumerate(csv):
                track_dict = {
                    self.model.columns[i]: v
                }
                converted_track.update(track_dict)
            logger_pro.info({
                'action': 'Convert csv list into track dict',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Convert csv list into track dict',
                'status': 'Fails',
                'message': '',
                'exception': e,
                'data': {
                    'csv': csv
                }
            })
        return converted_track
    
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
        """ Convert tracks into name and artist.

        Parameters
        ----------
        tracks: list
            A tracks list converted into a list 
            containing dict which key are name and artist.

        Raises
        ------
        Exception
            If it fails to convert them.

        Return
        ------
        converted_tracks: list
            A tracks list converted into a list 
            containing dict which keys are name and artist.
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
                'action': 'Convert tracks into name and artist',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'length': len(tracks),
                    'tracks': tracks
                }
            })
        return converted_tracks

    def convert_track_into_name_and_artist(self, track: dict) -> dict:
        """ Convert track into name and artist.

        Parameters
        ----------
        tracks: dict
            A track dict converted into a dict 
            containing name and artist.

        Raises
        ------
        Exception
            If it fails to convert it.

        Return
        ------
        converted_tracks: list
            A track dict converted into a dict 
            containing name and artist.
        """
        converted_track = []
        logger_pro.info({
            'action': 'Convert track into name and artist',
            'status': 'Run',
            'message': ''
        })
        try:
            converted_tracks = {
                'name': track['name'], 
                'artist': track['artist']
            }
            logger_pro.info({
                'action': 'Convert track into name and artist',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Convert track into name and artist',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'track': track
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

    def show_track(self, track: dict) -> None:
        """ Show a track if there is the track on CSV

        Parameters
        ----------
        track: dict
            A track dict to show.

        Raises
        ------
        Exception
            If it fails to show.

        Return
        ------
        None
        """
        track_from_csv = self.repository.find_track_first(track)
        if track_from_csv:
            track = self.convert_csv_into_track_dict(track_from_csv)
        
        logger_pro.info({
            'action': 'Show track info',
            'status': 'Run',
            'message': '',
        })
    
        try:
            for column in self.model.columns:
                logger_con.info(f'{column}: {track[column]}')
            logger_pro.info({
                'action': 'Show track info',
                'status': 'Success',
                'message': '',
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Show track info',
                'status': 'Fail',
                'message': '',
                'data': {
                    'columns': self.model.columns,
                    'track': track
                }
            })
