import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from models.singleton import Singleton
import utils.setting as setting


logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')


class SpotifyModel(Singleton):
    conn = None

    def __init__(self):
        pass

    def connect(self) -> None:
        """ Connect spotify api by SpotifyOAuth.

        Parameters
        ----------
        None

        Raises
        ------
        Exception
            If it fails to connect spotify.

        Return
        ------
        spotify:
            a object to connect spotify.
        """
        # get api data from environment environment variables
        client_id = setting.CONFIG['SPOTIPY']['SPOTIPY_CLIENT_ID']
        client_secret = setting.CONFIG['SPOTIPY']['SPOTIPY_CLIENT_SECRET']
        redirect_uri = 'https://google.com'
        """
            Scope reference:    https://developer.spotify.com/documentation/general/guides/authorization/scopes/
                user-library-read
                playlist-modify-private
                user-read-recently-played   :    for get playlist information
                playlist-modify-public      :    for modify public playlist (remove songs from playlist)
                user-read-currently-playing :    for getting a current track
        """
        scope = 'user-library-read \
                 playlist-modify-private \
                 user-read-recently-played \
                 playlist-modify-public \
                 user-read-currently-playing'

        logger_con.info('Start connecting Spotify...')
        logger_pro.info({
            'action': 'Connect spotify api by SpotifyOAuth',
            'status': 'Run',
            'message': '',
            'data': {
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'scope': scope
            }
        })
        auth_manager = SpotifyOAuth(client_id=client_id,
                                    client_secret=client_secret,
                                    redirect_uri=redirect_uri,
                                    scope=scope,
                                    open_browser=False)

        try:
            # Connect spotify
            self.conn = spotipy.Spotify(auth_manager=auth_manager, language='en')
            logger_con.info('Succeed in connecting Spotify...')
            logger_pro.info({
                'action': 'Connect spotify api by SpotifyOAuth',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_con.error('Fail to connecting Spotify...')
            logger_pro.error({
                'action': 'Connect spotify api by SpotifyOAuth',
                'status': 'Fail',
                'message': e
            })
        return
