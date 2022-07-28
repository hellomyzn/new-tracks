import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from models.new_track import NewTrackModel
import utils.setting as setting
import utils.helper as helper

logger_pro = logging.getLogger('production')
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
        self.playlist_ids = ["37i9dQZEVXbMDoHDwVN2tF", "37i9dQZEVXbLRQDuF5jeBp"]
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
        """ 
            Fetch tracks from multiple playlists.
            
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
        new_tracks_dict = []
        logger_pro.info({
            'action': 'Fetch tracks from multiple playlists.',
            'status': 'Run',
            'message': ''
        })
        for p_id in self.playlist_ids:
            try:
                tracks_json = self.fetch_tracks_json_from_playlist(p_id)
                tracks_dict = self.extract_tracks_from_json(tracks_json)
                tracks_dict = self.put_playlist_data_to_tracks_dict(p_id, tracks_dict)
                tracks_dict = self.retrieve_unique_tracks_dict(tracks_dict, new_tracks_dict)
                new_tracks_dict += tracks_dict
                logger_pro.debug({
                    'action': 'Fetch tracks from multiple playlists.',
                    'status': 'Success',
                    'message': '',
                    'data': {
                        'id': p_id,
                        'p_tracks_len': len(tracks_dict),
                        'tracks_len': len(new_tracks_dict)
                    }
                })
            except Exception as e:
                logger_con.error(f"Stoped while fetching tracks:': ({e})")
                logger_pro.error({
                    'action': 'Fetch tracks from multiple playlists.',
                    'status': 'Fail',
                    'message': '',
                    'exception': e,
                    'data': {
                        'playlist_id': p_id
                    }
                })
                return []
        logger_pro.info({
            'action': 'Fetch tracks from multiple playlists.',
            'status': 'Success',
            'message': ''
        })
        new_tracks = self.convert_tracks_dict_into_new_tracks(new_tracks_dict)
        return new_tracks
    
    def fetch_tracks_json_from_playlist(self, playlist_id: str) -> list:
        """ 
            Fetch tracks json data from a playlist.
            
            Parameters
            ----------
            playlist_id: str
                A playlist ID to fetch tracks from.

            Raises
            ------
            Exception
                The playlist id you provided is not correct.

            Return
            ------
            tracks: list
                A tracks json data list gotten from the playlist.
        """
        logger_pro.info({
            'action': f'Fetch tracks json data from a playlist ({playlist_id}).',
            'status': 'Run',
            'message': ''
        })
        tracks_number = self.fetch_playlist_track_number(playlist_id)
        max_number = 100
        tracks_json = []

        try:
            while max_number < tracks_number:
                offset = len(tracks_json)
                playlist_items = self.connect.playlist_items(playlist_id, limit=100, offset=offset)
                current_tracks_json = playlist_items['items']
                tracks_json += current_tracks_json
                tracks_number -= len(current_tracks_json)
                logger_pro.debug({
                    'action': f'Fetch tracks json data from a playlist ({playlist_id}).',
                    'status': 'Success',
                    'message': '',
                    'data': {
                        'offset': offset,
                        'until': offset + len(current_tracks_json),
                        'length': len(current_tracks_json)
                    }
                })
            else:
                # after while loop
                offset = len(tracks_json)
                playlist_items = self.connect.playlist_items(playlist_id, limit=100, offset=offset)
                current_tracks_json = playlist_items['items']
                tracks_json += current_tracks_json
                logger_pro.debug({
                    'action': f'Fetch tracks json data from a playlist ({playlist_id}).',
                    'status': 'Success',
                    'message': '',
                    'data': {
                        'offset': offset,
                        'until': offset + len(current_tracks_json),
                        'length': len(current_tracks_json)
                    }
                })
        except Exception as e:
            logger_pro.error({
                'action': f'Fetch tracks json data from a playlist ({playlist_id}).',
                'status': 'Fail',
                'message': 'This is in a while loop',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id
                }
            })
            raise Exception

        return tracks_json

    def fetch_playlist_track_number(self, playlist_id: str) -> int:
        """
            Fetch a playlist track number.

            Parameters
            ----------
            playlist_id: str
                A playlist ID to fetch tracks from.

            Raises
            ------
            Exception
                If you can not fetch playlist track number through Spotify API.

            Return
            ------
            track_number: int
                The number of tracks in a playlist.
        """
        logger_pro.info({
            'action': f'Fetch a playlist track number. ({playlist_id}) ',
            'status': 'Run',
            'message': ''
        })
        try:
            playlist_data = self.connect.playlist(playlist_id)
            track_number = playlist_data['tracks']['total']
            logger_pro.info({
                'action': f'Fetch a playlist track number. ({playlist_id}) ',
                'status': 'Success',
                'message': '',
                'data': {
                    'track_number': track_number
                }
            })
            return track_number
        except Exception as e:
            logger_pro.error({
                'action': f'Fetch a playlist track number. ({playlist_id}) ',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id
                }
            })
            raise Exception

    def fetch_playlist_name(self, playlist_id: str) -> str:
        """ 
            Fetch a playlist name.

            Parameters
            ----------
            playlist_id: str
                A playlist ID to fetch tracks from.

            Raises
            ------
            Exception
                If you can not fetch playlist name through Spotify API.

            Return
            ------
            playlist_name: str
                A playlist name.
        """
        logger_pro.info({
            'action': f'Fetch a playlist name ({playlist_id}) ',
            'status': 'Run',
            'message': ''
        })
        try:
            playlist_data = self.connect.playlist(playlist_id)
            playlist_name = playlist_data["name"]
            logger_pro.info({
                'action': f'Fetch a playlist name ({playlist_id}) ',
                'status': 'Success',
                'message': '',
                'data': {
                    'playlist_name': playlist_name
                }
            })
            return playlist_name
        except Exception as e:
            logger_pro.error({
                'action': f'Fetch a playlist name ({playlist_id}) ',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id
                }
            })
            raise Exception

    def fetch_playlist_url(self, playlist_id: str) -> str:
        """
            Fetch a playlist url

            Parameters
            ----------
            playlist_id: str
                A playlist ID to fetch tracks from.

            Raises
            ------
            Exception
                If you can not fetch playlist url through Spotify API

            Return
            ------
            playlist_url: str
                A playlist url
        """
        logger_pro.info({
            'action': f'Fetch a playlist url ({playlist_id}) ',
            'status': 'Run',
            'message': ''
        })
        try:
            playlist_data = self.connect.playlist(playlist_id)
            playlist_url = playlist_data['external_urls']['spotify']
            logger_pro.info({
                'action': f'Fetch a playlist url ({playlist_id}) ',
                'status': 'Success',
                'message': '',
                'data': {
                    'playlist_url': playlist_url
                }
            })
            return playlist_url
        except Exception as e:
            logger_pro.error({
                'action': f'Fetch a playlist url ({playlist_id}) ',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id
                }
            })
            raise Exception

    def extract_tracks_from_json(self, tracks_json: list) -> list:
        """ 
            Extract tracks from tracks json data.

            Parameters
            ----------
            tracks_json_data: dict
                A tracks json data.
            playlist_name: str, optional
                A playlist name to add to each track dict.
            playlist_url: str, optional
                A playlist url to add to each track dict.

            Raises
            ------
            Exception
                If it fail to extract track data.

            Return
            ------
            track: list
                A tracks list with dict having certain keys.
        """
        logger_pro.info({
            'action': f'Extract tracks from tracks json data.',
            'status': 'Run',
            'message': ''
        })
        tracks = []
        try:
            tracks = [self.extract_track_from_json(t) for t in tracks_json]
            logger_pro.info({
                'action': f'Extract tracks from tracks json data.',
                'status': 'Success',
                'message': '',
                'data': {
                    'tracs_len': len(tracks)
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': f'Extract tracks from tracks json data.',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id,
                    'len_tracks_json': len(tracks_json)
                }
            })
            raise Exception
        return tracks

    def extract_track_from_json(self, track_json: list) -> dict:
        """ 
            Extract track a track from tracks json data.

            Parameters
            ----------
            tracks_json_data: dict
                A track json data.

            Raises
            ------
            Exception
                If it fail to extract track data.

            Return
            ------
            track: dict
                A track dict with certain keys
        """
        logger_pro.debug({
            'action': 'Extract a track from tracks json data.',
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
            logger_pro.debug({
                'action': 'Extract a track from tracks json data.',
                'status': 'Success',
                'message': '',
                'track': track
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Extract a track from tracks json data.',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'track_json': track_json
                }
            })
            raise Exception
        return track

    def put_playlist_data_to_tracks_dict(self, playlist_id: str, tracks_dict: list) -> list:
        """ 
            Put playlist name and url to tracks dict

            Parameters
            ----------
            playlist_id: str
                A playlist id to add to the tracks dict
            tracks_dict: list
                A tracks dict of list.

            Raises
            ------
            Exception
                If it fail to put playlist data to the tracks dict.

            Return
            ------
            tracks: list
                A track dict of list added name and url.
        """
        logger_pro.info({
            'action': 'Put playlist name and url to tracks dict',
            'status': 'Run',
            'message': ''
        })
        tracks = []
        try:
            p_name = self.fetch_playlist_name(playlist_id)
            p_url = self.fetch_playlist_url(playlist_id)
            tracks = [self.put_playlist_data_to_track_dict(t, p_name, p_url) for t in tracks_dict]
            logger_pro.info({
                'action': 'Put playlist name and url to tracks dict',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Put playlist name and url to tracks dict',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'playlist_id': playlist_id,
                    'tracks_dict': tracks_dict
                }
            })
            raise Exception
        return tracks

    def put_playlist_data_to_track_dict(self, 
                                        track_dict: dict,
                                        p_name: str,
                                        p_url: str) -> dict:
        """ 
            Put playlist name and url to a track dict

            Parameters
            ----------
            tracks_dict: dict
                A tracks dict without playlist data.
            p_name: str
                A playlist name to add
            p_url: str
                A playlist url to add

            Raises
            ------
            Exception
                If it fail to put playlist data to the tracks dict.

            Return
            ------
            tracks: dict
                A track dict added playlist data.
        """
        logger_pro.debug({
            'action': 'Put playlist name and url to a track dict',
            'status': 'Run',
            'message': ''
        })
        try:
            track_dict['playlist_name'] = p_name
            track_dict['playlist_url'] = p_url
            logger_pro.debug({
                'action': 'Put playlist name and url to a track dict',
                'status': 'Success',
                'message': '',
                'track_dict': track_dict
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Put playlist name and url to a track dict',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'track_dict': track_dict
                }
            })
            raise Exception
        return track_dict

    def retrieve_unique_tracks_dict(self, tracks: list, from_tracks: list) -> list:
        """
            Retrieve unique tracks dict from tracks dict

            Parameters
            ----------
            tracks: list
                A tracks list to confirm It's unique or no.
            from_tracks: list
                A tracks list to confirm from.

            Raises
            ------
            Exception
                If it fail to retrieve

            Return
            ------
            unique_tracks: list
                a unique tracks list.
        """
        logger_pro.info({
            'action': 'Retrieve unique tracks dict from tracks dict',
            'status': 'Run',
            'message': ''
        })
        
        if not from_tracks:
            logger_con.info(f'The number of new tracks is {len(tracks)}')
            logger_pro.info({
                'action': 'Retrieve unique tracks dict from tracks dict',
                'status': 'Success',
                'message': '',
                'data': {
                    'tracks_len': len(tracks)
                }
            })
            return tracks

        unique_tracks = []
        try:
            from_track_names = [t['name'] for t in from_tracks]
            from_track_artists = [t['artist'] for t in from_tracks]
            for track in tracks:
                if track['name'] in from_track_names and track['artist'] in from_track_artists:
                    continue
                unique_tracks.append(track)
            
            logger_con.info(f'The number of new tracks is {len(unique_tracks)}')
            logger_pro.info({
                'action': 'Retrieve unique tracks dict from tracks dict',
                'status': 'Success',
                'message': '',
                'data': {
                    'tracks_len': len(tracks)
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Retrieve unique tracks dict from tracks dict',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'tracks_len': len(tracks),
                    'from_tracks_len': len(from_tracks),
                    'tracks': tracks,
                    'from_tracks': from_tracks
                }
            })
            raise Exception
        return unique_tracks

    def convert_tracks_dict_into_new_tracks(self, tracks_dict) -> NewTrackModel:
        """
            Convert tracks dict into new tracks model

            Parameters
            ----------
            tracks_dict: dict
                A tracks dict

            Raises
            ------
            Exception
                If it fail to convert

            Return
            ------
            new_tracks: NewTrackModel
                new_tracks model put each columns data
        """
        logger_pro.info({
            'action': 'Convert tracks dict into new tracks model',
            'status': 'Run',
            'message': ''
        })
        new_tracks = []
        try:
            for t_dic in tracks_dict:
                new_track = NewTrackModel(t_dic['name'],
                                          t_dic['artist'],
                                          t_dic['playlist_name'],
                                          t_dic['track_url'],
                                          t_dic['playlist_url'],
                                          t_dic['added_at'],
                                          t_dic['created_at'],
                                          t_dic['like'])
                new_tracks.append(new_track)
                logger_pro.debug({
                    'action': 'Convert tracks dict into new tracks model',
                    'status': 'Success',
                    'message': '',
                    'data': {
                        'new_track': new_track
                    }
                })
            logger_pro.info({
                'action': 'Convert tracks dict into new tracks model',
                'status': 'Success',
                'message': '',
                'data': {
                    'new_tracks_len': len(new_tracks)
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Convert tracks dict into new tracks model',
                'status': 'Fails',
                'exception': e,
                'data': {
                    'tracks_dict': tracks_dict
                }
                
            })
            raise Exception
        return new_tracks

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
