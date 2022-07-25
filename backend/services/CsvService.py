""" """
import logging

from models.Csv import Csv
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
        model:
            A csv model
        repository:
            A csv repository
        """
        self.model = Csv()
        self.repository = CsvRepository(setting.FILE_PATH_OF_CSV)

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
        if not helper.exists_file(path):
            return []
        if not self.repository.read_header(path):
            return []

        track = CsvRepository.get_first_data_by_name_and_artist(path,
                                                                name,
                                                                artist)
        return track

    def write_tracks(self, csv_file_path, tracks: list) -> None:
        # Check there is csv file
        if not helper.exists_file(csv_file_path):
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

    def read_tracks(self) -> list:
        """ Read tracks data from CSV.
        
        If there is no file or there is no any track data,
        return a empty list.

        Parameters
        ----------
        None
        
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

        if not helper.exists_file(self.repository.path):
            return []

        if not self.repository.read_header():
            return []

        tracks = []
        tracks_list = self.repository.read()

        logger_pro.info({
            'action': 'Retrieve tracks data from csv',
            'status': 'Run',
            'message': '',
            'data': {
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

    def distinct_tracks_by_csv(self, tracks: list) -> list:
        """ distinct tracks by csv
        
        Parameters
        ----------
        tracks: list
            A tracks data

        Raises
        ------
        TypeError
            The playlist id you provided is not correct.

        Return
        ------
        new_tracks: list
            A new tracks list from tracks data which doesn't exist 
            in the tracks_from_csv
                
        """
        tracks_only_name_artist_from_csv = []
        tracks_only_name_artist_from_spotify = []
        new_tracks = []
        
        tracks_from_csv = self.read_tracks()

        logger_pro.info({
            'action': 'Select new tracks from csv tracks data',
            'status': 'Run',
            'message': '',
            'args': {
                'tracks': tracks,
                'tracks_from_csv': tracks_from_csv
            }
        })

        # If there is no track data, it regards all tracks as new tracks
        if not tracks_from_csv:
            logger_con.info(f'The number of new tracks is {len(new_tracks)}')
            logger_pro.warning({
                'action': 'Select new tracks from csv tracks data',
                'status': 'Warning',
                'message': 'There is no tracks data in on csv ',
                'args': {
                    'tracks': tracks,
                    'tracks_from_csv': tracks_from_csv
                }
            })

            return tracks

        # Prepare a list from csv to check which tracks are new for this time
        for track in tracks_from_csv:
            tracks_only_name_artist_from_csv.append({
                'name': track['name'],
                'artist': track['artist']
            })

        # Prepare a list from retrieved tracks to check which tracks are new for this time
        for track in tracks:
            tracks_only_name_artist_from_spotify.append({
                'name': track['name'],
                'artist': track['artist']
            })

        # Check which tracks are new
        for i, track in enumerate(tracks_only_name_artist_from_spotify):
            if track in tracks_only_name_artist_from_csv:
                continue
            new_tracks.append(tracks[i])

        logger_con.info(f'The number of new tracks is {len(new_tracks)}')
        logger_pro.info({
            'action': 'Select new tracks from csv tracks data',
            'status': 'Success',
            'message': '',
            'data': {
                'track': new_tracks
            }
        })

        return new_tracks
