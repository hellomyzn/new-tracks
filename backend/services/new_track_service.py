import logging
import time

from models.spotify import SpotifyModel
from repositories.new_track.spotify import SpotifyNewTrackRepository
from repositories.new_track.csv import CsvNewTrackRepository
from repositories.new_track.google_spreadsheet import GssNewTrackRepository
import utils.helper as helper

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')

class NewTrackService(object):
    """
    A class used to represent a spotify service.

    Attributes
    ----------
    spotify:
        A spotify new track repository.
    csv:
        A csv new track repository.
    gss:
        A google spreadsheet new track repository.

    Methods
    ------
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        self.spotify = SpotifyModel()
        self.playlist_ids = [
            "37i9dQZEVXbMDoHDwVN2tF",  # GLOBAL
            "37i9dQZEVXbLRQDuF5jeBp",  # US
            "37i9dQZEVXbKXQ4mDTEBXq",  # JP
            "37i9dQZEVXbNBz9cRCSFkY",  # PH
            "37i9dQZEVXbLZ52XmnySJg",  # IN
            "37i9dQZEVXbLnolsZ8PSNw",  # UK
            "37i9dQZEVXbNxXF4SkHj9F",  # KR
            "37i9dQZEVXbNFJfN1Vw8d9",  # SP
            "37i9dQZEVXbJPcfkRz0wJ0",  # AU
            "37i9dQZEVXbJiZcmkrIHGU",  # GE
            "37i9dQZEVXbIQnj7RRhdSX",  # IT
            "37i9dQZEVXbIPWwFssbupI",  # FR
            "37i9dQZEVXbMXbN3EUUhlg",  # BR
            "37i9dQZF1DX4JAvHpjipBk"   # New Music Friday
            ]

    def add_new_tracks(self) -> None:
        """ Add new tracks to csv, gss, spotify playlist
        
        Parameters
        ----------
        None

        Raises
        ------
        None

        Return
        ------
        None
        """
        spotify_repo = SpotifyNewTrackRepository()
        csv_repo = CsvNewTrackRepository()
        gss_repo =  GssNewTrackRepository()

        # Fetch tracks from playlists
        tracks_spotify = self.fetch_tracks_from_playlists()                
        tracks_csv = csv_repo.all()
        
        new_tracks = self.retrieve_unique_tracks_dict(tracks_spotify,tracks_csv)

        for track in new_tracks:
            spotify_repo.add(track)
            csv_repo.add(track)
            gss_repo.add(track)
        return

    def fetch_tracks_from_playlists(self) -> list:
        """ 
            Fetch tracks from multiple playlists.
            
            Parameters
            ----------
            None

            Raises
            ------
            Exception:
                If it fails to fetch tracks from playlists, return an empty list.

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
        try:
            for p_id in self.playlist_ids:
                tracks_json = self.fetch_tracks_json_from_playlist(p_id)
                tracks_dict = self.extract_tracks_from_json(tracks_json)
                tracks_dict = self.retrieve_unique_tracks_dict(tracks_dict, new_tracks_dict)
                tracks_dict = self.put_playlist_data_to_tracks_dict(p_id, tracks_dict)
                new_tracks_dict += tracks_dict
                logger_pro.debug({
                    'action': 'Fetch tracks from multiple playlists.',
                    'status': 'Success',
                    'message': 'This is in a for loop',
                    'data': {
                        'id': p_id,
                        'p_tracks_len': len(tracks_dict),
                        'tracks_len': len(new_tracks_dict)
                    }
                })
        except Exception as e:
            new_tracks_dict = []
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

        logger_pro.info({
            'action': 'Fetch tracks from multiple playlists.',
            'status': 'Success',
            'message': ''
        })
        
        return new_tracks_dict
    
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
                playlist_items = self.spotify.connect.playlist_items(playlist_id, limit=100, offset=offset)
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
                # after while loop or less than 100 tracks
                offset = len(tracks_json)
                playlist_items = self.spotify.conn.playlist_items(playlist_id, limit=100, offset=offset)
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
            playlist_data = self.spotify.conn.playlist(playlist_id)
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
            playlist_data = self.spotify.conn.playlist(playlist_id)
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
            playlist_data = self.spotify.conn.playlist(playlist_id)
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

    def extract_track_from_json2(self, track_json: list) -> dict:
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
                'name': track_json['name'],
                'artist': track_json['artists'][0]['name'],
                'playlist_name': None,
                'track_url': track_json['external_urls']['spotify'],
                'playlist_url': None,
                'release_date': track_json["album"]["release_date"],
                'added_at': None,
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
            'message': '',
            'data': {
                'tracks_len': len(tracks),
                'from_tracks_len': len(from_tracks)
            }
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
                    'tracks_len': len(unique_tracks)
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

    def show_current_track(self) -> None:
        """
            Show current track you are listening.

            Parameters
            ----------
            None
            
            Raises
            ------
            Exception
                If you can not show current track

            Return
            ------
            None  
        """
        track = self.fetch_playing_track()
        logger_con.info(f'Track: {track["name"]}')  
        logger_con.info(f'Artist: {track["artist"]}')
        return None

    def fetch_playing_track(self) -> dict:
        """ 
            Fetch a track data you are listening.

            if there is no track you are listening,
            return empty list.

            Parameters
            ----------
            None
            
            Raises
            ------
            Exception
                If you can not fetch current track.

            Return
            ------
            track: dict
                A track you are listening.
        """
        track_json = self.spotify.conn.current_user_playing_track()
        
        if track_json:
            track_json = track_json['item']
            track = self.extract_track_from_json2(track_json)
        else:
            track = []
            message = 'There is no current track you are listening on Spotify right now'
            logger_con.warning(message)
            logger_pro.warning(message)
        return track

    def remove_current_tracks(self) -> None:
        """ 
            remove tracks you listened currently on Spotify.

            Parameters
            ----------
            None.
            
            Raises
            ------
            Exception
                If you can not remove.

            Return
            ------
            None.
        """
        # Fetch tracks json data you listened currently
        tracks_json = self.fetch_current_tracks_json_data()
        # Extract tracks from json
        tracks_json = tracks_json['items']
        tracks_dict = []
        for t in tracks_json:
            track_dict = self.extract_track_from_json2(t['track'])
            logger_con.info(f'Curent Track: {track_dict["name"]}')
            tracks_dict.append(track_dict)
        # Remove tracks
        spotify_repo = SpotifyNewTrackRepository()
        for t in tracks_dict:
            spotify_repo.delete_track_by_url(t['track_url'])

        return None

    def fetch_current_tracks_json_data(self) -> dict:
        """ 
            Fetch a track data you are listening.

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
        logger_pro.debug({
            'action': 'Fetch current track data from spotify',
            'status': 'Run',
            'message': ''
        })

        try:
            track_json = self.spotify.conn.current_user_recently_played()
            logger_pro.debug({
                'action': 'Fetch current track data from spotify',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            track_json = []
            logger_pro.warning({
                'action': 'Fetch current track data from spotify',
                'status': 'Fail',
                'message': '',
                'exception': e
            })
        return track_json

    def remove_tracks_by_index(self, first, last) -> None:
        """ 
            remove tracks by index (first, last) you choose.

            Parameters
            ----------
            first: int
                The index number of playlist from.
            last: int
                The index number of playlist until.
            
            Raises
            ------
            Exception
                If you can not remove.

            Return
            ------
            None.
        """
        # Fetch tracks from playlist
        spotify_repo = SpotifyNewTrackRepository()
        tracks_dict = spotify_repo.all()
        tracks_dict = tracks_dict[first-1:last]
        
        # Remove tracks
        for t in tracks_dict:
            spotify_repo.delete_track_by_url(t['track_url'])
        return None
