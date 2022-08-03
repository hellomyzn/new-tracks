import logging

import utils.setting as setting
from models.interfaces.new_track import NewTrack

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')

class NewTrackModel(NewTrack):
    def __init__(self):
        self.name = None
        self.artist = None
        self.playlist_name = None
        self.track_url = None
        self.playlist_url = None
        self.release_date = None
        self.added_at = None
        self.created_at = None
        self.like = None
    
    def get_columns(self) -> list:
        columns = [
            'name',
            'artist',
            'playlist_name',
            'track_url',
            'playlist_url',
            'release_date',
            'added_at',
            'created_at',
            'like'
            ]
        return columns
    
    def get_dict(self) -> dict:
        """ 
            Get track dict data.
            
            Parameters
            ----------
            None

            Raises
            ------
            Exception
                If you can not get.

            Return
            ------
            track: dict
                A track dict data.
        """
        logger_pro.debug({
            'action': 'Get track dict data.',
            'status': 'Run',
            'message': ''
        })
        try:
            track = {
                'name': self.name,
                'artist': self.artist,
                'playlist_name': self.playlist_name,
                'track_url': self.track_url,
                'playlist_url': self.playlist_url,
                'release_date': self.release_date,
                'added_at': self.added_at,
                'created_at': self.created_at,
                'like': self.like
            }
            logger_pro.debug({
                'action': 'Get track dict data.',
                'status': 'Success',
                'message': '',
                'track': track
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Get track dict data.',
                'status': 'Success',
                'message': '',
                'exception': e
            })
            raise Exception
        return track

    def set_columns(self, tracks_dict: dict) -> None:
        """ 
            Set dict data up columns.
            
            Parameters
            ----------
            tracks_dict: dict
                A dict to set up

            Raises
            ------
            Exception
                If you can not set up.

            Return
            ------
            None.
        """
        logger_pro.debug({
            'action': 'Set dict data up columns.',
            'status': 'Run',
            'message': ''
        })
        try:

            self.name = tracks_dict['name']
            self.artist = tracks_dict['artist']
            self.playlist_name = tracks_dict['playlist_name']
            self.track_url = tracks_dict['track_url']
            self.playlist_url = tracks_dict['playlist_url']
            self.release_date = tracks_dict['release_date']
            self.added_at = tracks_dict['added_at']
            self.created_at = tracks_dict['created_at']
            self.like = tracks_dict['like']

            logger_pro.debug({
                'action': 'Set dict data up columns.',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Set dict data up columns.',
                'status': 'Fail',
                'message': ''
            })
            raise Exception
        return None

