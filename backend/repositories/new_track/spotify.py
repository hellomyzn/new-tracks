import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from models.new_track import NewTrackModel
import utils.setting as setting
import utils.helper as helper

logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')

class SpotifyNewTrackRepository(object):
    """
    A class used to represent a spotify repository.

    Attributes
    ----------
    model:
        A spotify model.
    playlist_ids: list
        Playlist ids for input.
    my_playlist_id: str
        A playlist id for output 
    connect:
        An instance to connect spotify API.

    Methods
    -------
    """
    def __init__(self):
        """
        Parameters
        ----------
        model:
            A spotify model
        """
        self.model = NewTrackModel()
        # self.playlist_ids = [
        #     "37i9dQZEVXbMDoHDwVN2tF",  # GLOBAL
        #     "37i9dQZEVXbLRQDuF5jeBp",  # US
        #     "37i9dQZEVXbKXQ4mDTEBXq",  # JP
        #     "37i9dQZEVXbNBz9cRCSFkY",  # PH
        #     "37i9dQZEVXbLZ52XmnySJg",  # IN
        #     "37i9dQZEVXbLnolsZ8PSNw",  # UK
        #     "37i9dQZEVXbNxXF4SkHj9F",  # KR
        #     "37i9dQZEVXbNFJfN1Vw8d9",  # SP
        #     "37i9dQZEVXbJPcfkRz0wJ0",  # AU
        #     "37i9dQZEVXbJiZcmkrIHGU",  # GE
        #     "37i9dQZEVXbIQnj7RRhdSX",  # IT
        #     "37i9dQZEVXbIPWwFssbupI",  # FR
        #     "37i9dQZEVXbMXbN3EUUhlg",  # BR
        #     "37i9dQZF1DX4JAvHpjipBk"   # New Music Friday
        # ]
        self.playlist_ids = ["74ADq6td6OPgGD8fhihTBm", "1gJIaZ9p6Q9awFopFxC74G"]
        self.my_playlist_id = setting.CONFIG['PLAYLIST_ID']['MY_PLAYLIST']
        self.connect = SpotifyNewTrackRepository.connect()
    
    @classmethod
    def connect(cls):
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
            spotify = spotipy.Spotify(auth_manager=auth_manager, language='en')
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
        return spotify

    def fetch_tracks_from_playlists(self) -> list:
        """ Fetch tracks from multiple playlists.
        
        Parameters
        ----------
        None

        Raises
        ------
        None

        Return
        ------
        tracks: list
            A tracks list
        """
        tracks = []
        for p_id in self.playlist_ids:

            tracks = self.fetch_tracks_from_playlist(p_id)
            print(len(tracks))

        return tracks

    def fetch_tracks_from_playlist(self, playlist_id: str) -> list:
        """ Fetch tracks from a playlist.
        
        Parameters
        ----------
        playlist_id: str
            A playlist ID to fetch tracks from.

        Raises
        ------
        TypeError
            The playlist id you provided is not correct.
        Exception


        Return
        ------
        tracks: list
            A tracks data list gotten from the playlist.
        """
        playlist_json_data = self.fetch_playlist_json_data(playlist_id)
        max_number = 100
        tracks_number = playlist_json_data['tracks']['total']
        tracks_json = []

        # logger_con.info(f'Retrieve tracks data from playlist: {playlist_name}: {tracks_number}')
        while max_number < tracks_number:
            offset = len(tracks_json)
            tracks_json += self.fetch_playlist_items_json_data(playlist_id, offset=offset)
            tracks_number -= len(tracks_json) - offset
        else:
            # after while loop
            offset = len(tracks_json)
            tracks_json += self.fetch_playlist_items_json_data(playlist_id, offset=offset)

        tracks = []
        playlist_name = playlist_json_data["name"]
        playlist_url = playlist_json_data['external_urls']['spotify']

        for t_json in tracks_json:
            track = self.extract_track_from_json(t_json)
            track['playlist_name'] = playlist_name
            track['playlist_url'] = playlist_url
            tracks.append(track)
        return tracks
    
    def fetch_playlist_json_data(self, playlist_id: str) -> list:
        """ Fetch a playlist json data

        Parameters
        ----------
        playlist_id: str
            A playlist ID to fetch tracks from.

        Raises
        ------
        Exception
            If you can not fetch playlist json data through Spotify API

        Return
        ------
        playlist_data: list
            A playlist json data

        """

        playlist_data = []
        logger_pro.info({
            'action': 'Get playlist json data',
            'status': 'Run',
            'message': ''
        })
        try:
            playlist_data = self.connect.playlist(playlist_id)
            logger_pro.info({
                'action': 'Get playlist json data',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Get playlist json data',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id
                }
            })
        return playlist_data

    def fetch_playlist_items_json_data(self, playlist_id: str, offset: int=0) -> list:
        """ Fetch a playlist items json data

        Parameters
        ----------
        playlist_id: str
            A playlist ID to fetch tracks from.
        offset: int, optional
            the index of the first item to return. (default is 0)
        Raises
        ------
        Exception
            If you can not fetch playlist items json data through Spotify API

        Return
        ------
        playlist_items: list
            A playlist items json data

        """
        playlist_items = []
        additional_types = ['track', 'episode']
        logger_pro.info({
            'action': 'Fetch a playlist items json data',
            'status': 'Run',
            'message': ''
        })
        try:
            playlist_items_json = self.connect.playlist_items(playlist_id, 
                                                         fields=None, 
                                                         limit=100, 
                                                         offset=offset, 
                                                         market=None, 
                                                         additional_types=additional_types)
            playlist_items = playlist_items_json['items']
            logger_pro.info({
                'action': 'Fetch a playlist items json data',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_pro.warning({
                'action': 'Fetch a playlist items json data',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id,
                    'offset': offset
                }
            })
        
        return playlist_items

    def extract_track_from_json(self, track_json) -> list:
        """ Extract only tracks data from tracks json data.

        Parameters
        ----------
        tracks_json_data: dict
            A tracks json data.

        Raises
        ------
        Exception
            If it fail to extract track data.

        Return
        ------
        track: list
            A track list with certain keys
        """
        logger_pro.info({
            'action': 'Extract only tracks data from tracks json data.',
            'status': 'Run',
            'message': ''
        })
        try:
            track = {
                'name': track_json['track']['name'],
                'artist': track_json['track']['artists'][0]['name'],
                'playlist_name': None,
                'track_url': track_json['track']['external_urls']['spotify'],
                'playlist_url': None,
                'release_date': track_json["track"]["album"]["release_date"],
                'added_at': track_json['added_at'],
                'created_at': helper.get_date(),
                'like': False
            }
            logger_pro.info({
                'action': 'Extract only tracks data from tracks json data.',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Extract only tracks data from tracks json data.',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'track_json': track_json
                }
            })
        return track

    def add_tracks_to_playlist(self, track_urls: list, playlist_id: str) -> None:
        """ Add tracks to a playlist.

        Parameters
        ----------
        track_urls: list
            A list of track urls to add
        
        Raises
        ------
        Exception
            If you can not add tracks to the playlist

        Return
        ------
        None
        """
        logger_pro.info({
            'action': 'Add tracks to a playlist',
            'status': 'Run',
            'message': '',
            'args': {
                'length': len(track_urls),
                'track_urls': track_urls,
                'playlist_id': self.my_playlist_id
            }
        })
        try:
            self.connect.playlist_add_items(self.my_playlist_id, track_urls, position=0)
            logger_pro.info({
                'action': 'Add tracks to a playlist',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_pro.warning({
                'action': 'Add tracks to a playlist',
                'status': 'Fail',
                'message': '',
                'exception': e
            })
        return

    def fetch_current_track_json_data(self) -> list:
        """ Fetch a track data you are listening.

        Parameters
        ----------
        None
        
        Raises
        ------
        Exception
            If you can not fetch current track.

        Return
        ------
        track: list
            A track you are listening.
        """
        logger_pro.info({
            'action': 'Fetch current track data from spotify',
            'status': 'Run',
            'message': ''
        })

        try:
            track_json_data = self.connect.current_user_playing_track()
            logger_pro.info({
                'action': 'Fetch current track data from spotify',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            track_json_data = []
            logger_pro.warning({
                'action': 'Fetch current track data from spotify',
                'status': 'Fail',
                'message': '',
                'exception': e
            })
        return track_json_data

    def get_tracks_played_recently(self) -> list:
            tracks = []
            tracks_json_data = spotify.connect.current_user_recently_played()
            tracks_json_data = tracks_json_data['items']
            return tracks_json_data

    def remove_tracks_from_playlist(self, playlist_id: str, tracks: list) -> None:
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
            self.connect.playlist_remove_all_occurrences_of_items(playlist_id, items)
            print("It's removed")
        else:
            print("It's cancelled")
        return
