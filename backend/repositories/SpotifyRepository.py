import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import utils.setting as setting
import utils.helper as helper


class SpotifyRepository(object):
    def __init__(self):
        self.logger_pro = logging.getLogger('production')
        self.logger_dev = logging.getLogger('develop')
        self.logger_con = logging.getLogger('console')
        self.connect = SpotifyRepository.connect(self.logger_pro, self.logger_dev, self.logger_con)
    
    @classmethod
    def connect(cls, logger_pro, logger_dev, logger_con):
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
            'message': ''
        })
        auth_manager = SpotifyOAuth(client_id=client_id,
                                        client_secret=client_secret,
                                        redirect_uri=redirect_uri,
                                        scope=scope,
                                        open_browser=False)

        try:
            # Connect spotify
            spotify = spotipy.Spotify(auth_manager=auth_manager)
            logger_con.info('Succeed in connecting Spotify...')
            logger_pro.info({
                'action': 'Connect spotify api by SpotifyOAuth',
                'status': 'Success',
                'message': '',
                'data': {
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': redirect_uri,
                    'scope': scope
                }
            })
        except Exception as e:
            logger_con.info('Fail to connecting Spotify...')
            self.logger_pro.error({
                'action': 'Connect spotify api by SpotifyOAuth',
                'status': 'Fail',
                'message': e,
                'data': {
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': redirect_uri,
                    'scope': scope
                }
            })
        return spotify

    def get_current_track_json_data(self) -> list:
        self.logger_pro.info({
            'action': 'Get current track data from spotify',
            'status': 'Run',
            'message': ''
        })

        try:
            track_json_data = self.connect.current_user_playing_track()
            self.logger_pro.info({
                'action': 'Get current track data from spotify',
                'status': 'Success',
                'message': '',
                'data': track_json_data
            })
        except Exception as e:
            track_json_data = []
            self.logger_pro.warning({
                'action': 'Get current track data from spotify',
                'status': 'Fail',
                'message': '',
                'exception': e
            })
        return track_json_data

    @staticmethod
    def get_tracks_played_recently(spotify) -> list:
        tracks = []
        tracks_json_data = spotify.connect.current_user_recently_played()
        tracks_json_data = tracks_json_data['items']
        return tracks_json_data

    def get_playlist_json_data(self, playlist_id: str) -> list:
        playlist_data = None
        self.logger_pro.info({
            'action': 'Get playlist json data',
            'status': 'Run',
            'message': '',
            'args': {
                'args': playlist_id
            }
        })
        try:
            playlist_data = self.connect.playlist(playlist_id)
            self.logger_pro.info({
                'action': 'Get playlist json data',
                'status': 'Success',
                'message': '',
                'data': playlist_data
            })
        except Exception as e:
            self.logger_pro.warning({
                'action': 'Get playlist json data',
                'status': 'Fail',
                'message': '',
                'exception': e
            })
        return playlist_data

    def get_playlist_items_json_data(self, playlist_id: str, offset=0) -> list:
        playlist_items = None
        self.logger_pro.info({
            'action': 'Get playlist items json data',
            'status': 'Run',
            'message': '',
            'args': {
                'playlist_id': playlist_id,
                'offset': offset
            }
        })
        try:
            playlist_items = self.connect.playlist_items(playlist_id, 
                                                         fields=None, 
                                                         limit=100, 
                                                         offset=offset, 
                                                         market=None, 
                                                         additional_types=('track', 'episode'))
            self.logger_pro.info({
                'action': 'Get playlist items json data',
                'status': 'Success',
                'message': '',
                'data': playlist_items
            })
        except Exception as e:
            self.logger_pro.warning({
                'action': 'Get playlist items json data',
                'status': 'Fail',
                'message': '',
                'exception': e
            })
        return playlist_items
            
    def add_tracks_to_playlist(self, playlist_id, urls):
        self.connect.playlist_add_items(playlist_id, urls, position=0)


    @staticmethod
    def remove_tracks_from_playlist(spotify, playlist_id, tracks) -> None:
        # TODO: if there are more than 100 tracks
        items = [track['track_url'] for track in tracks]
        names = [track['name'] for track in tracks]
        print('\n')
        for name in names:
            print(f'\t[TRACK NAME] - {name}')

        # TODO: If there is no track this time, return and print there is no track this time
        question = '\nDo you want to remove these tracks above from your playlist? [y/n]: '
        user_input = input(question)

        if helper.is_yes(user_input):
            spotify.connect.playlist_remove_all_occurrences_of_items(playlist_id, items)
            print("It's removed")
        else:
            print("It's cancelled")
        return
