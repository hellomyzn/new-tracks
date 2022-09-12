import logging
import time

from models.spotify import SpotifyModel
from models.new_track import NewTrackModel
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
        None

        Methods
        ------
    """

    def __init__(self):
        """
            Parameters
            ----------
            None
        """
        pass

    @classmethod
    def fetch_tracks_dict_from_playlists(cls) -> list:
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
        playlist_ids = [
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
            "37i9dQZF1DX4JAvHpjipBk",  # New Music Friday
            "37i9dQZF1DWZvuOKNcLsjv",  # Next up
            "37i9dQZEVXbfAlVIR3gQhM"   # Release Radar
        ]

        logger_pro.info({
            'action': 'Fetch tracks from multiple playlists.',
            'status': 'Run',
            'message': ''
        })

        try:
            for p_id in playlist_ids:
                # Fetch json data
                tracks_json = NewTrackService.fetch_tracks_json_from_playlist(p_id)
                # Extract only the data we need
                tracks_json = [t['track'] for t in tracks_json]
                # Remove None in the list
                tracks_json = filter(None, tracks_json)
                # Extract track data
                tracks_dict = [NewTrackService.extract_track_dict_from_json(t) for t in tracks_json]
                # Remove None from tracks_dict
                tracks_dict = [ t for t in tracks_dict if t is not None]
                # Remove duplicated tracks amoung the playlists
                if new_tracks_dict:
                    tracks_dict, _ = NewTrackService.retrieve_unique_and_duplicate_tracks_dict(tracks_dict, new_tracks_dict)
                # Put playlist data on tracks dict
                tracks_dict = NewTrackService.put_playlist_data_into_tracks_dict(p_id, tracks_dict)
                new_tracks_dict += tracks_dict
                logger_pro.info({
                    'action': 'Fetch tracks from a playlist.',
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
                'exception': e
            })
            raise Exception

        logger_pro.info({
            'action': 'Fetch tracks from multiple playlists.',
            'status': 'Success',
            'message': '',
            'new_tracks_dict_len': len(new_tracks_dict)
        })
        
        return new_tracks_dict
    
    @classmethod
    def fetch_tracks_json_from_playlist(cls, playlist_id: str) -> list:
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
        logger_pro.debug({
            'action': f'Fetch tracks json data from a playlist ({playlist_id}).',
            'status': 'Run',
            'message': ''
        })
        tracks_number = NewTrackService.fetch_playlist_track_number(playlist_id)
        max_number = 100
        tracks_json = []

        try:
            spotify = SpotifyModel()
            while max_number < tracks_number:
                offset = len(tracks_json)
                playlist_items = spotify.conn.playlist_items(playlist_id, limit=100, offset=offset)
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
                playlist_items = spotify.conn.playlist_items(playlist_id, limit=100, offset=offset)
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

    @classmethod
    def fetch_playlist_track_number(cls, playlist_id: str) -> int:
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
        logger_pro.debug({
            'action': f'Fetch a playlist track number. ({playlist_id}) ',
            'status': 'Run',
            'message': ''
        })
        try:
            spotify = SpotifyModel()
            playlist_data = spotify.conn.playlist(playlist_id)
            track_number = playlist_data['tracks']['total']
            logger_pro.debug({
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

    @classmethod
    def fetch_playlist_name(cls, playlist_id: str) -> str:
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
        logger_pro.debug({
            'action': f'Fetch a playlist name ({playlist_id}) ',
            'status': 'Run',
            'message': ''
        })
        try:
            spotify = SpotifyModel()
            playlist_data = spotify.conn.playlist(playlist_id)
            playlist_name = playlist_data["name"]
            logger_pro.debug({
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

    @classmethod
    def fetch_playlist_url(cls, playlist_id: str) -> str:
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
        logger_pro.debug({
            'action': f'Fetch a playlist url ({playlist_id}) ',
            'status': 'Run',
            'message': ''
        })
        try:
            spotify = SpotifyModel()
            playlist_data = spotify.conn.playlist(playlist_id)
            playlist_url = playlist_data['external_urls']['spotify']
            logger_pro.debug({
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

    @classmethod
    def fetch_current_tracks_json(cls) -> dict:
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
            spotify = SpotifyModel()
            track_json = spotify.conn.current_user_recently_played()
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

    @classmethod
    def fetch_playing_track_json(cls) -> dict:
        """ 
            Fetch a track json data you are listening.

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
        logger_pro.info({
            'action': 'Fetch a track json data you are listening.',
            'status': 'Run',
            'message': ''
        })
        try:
            spotify = SpotifyModel()
            track_json = spotify.conn.current_user_playing_track()
            logger_pro.info({
                'action': 'Fetch a track json data you are listening.',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Fetch a track json data you are listening.',
                'status': 'Fail',
                'message': '',
                'exception': e
            })
            raise Exception
        return track_json

    @classmethod
    def confirm_remove_tracks(cls, tracks: list) -> bool:
        """
            Confirm to remove tracks.

            If there is no tracks, return False

            Parameters
            ----------
            tracks: list
                A list of NewTrackModel instances to remove.
            
            Raises
            ------
            Warninig
                If there is no tracks.
            Exception
                If you can not confirm.
            
            Return
            ------
            Bool.
        """
        logger_pro.debug({
            'action': 'Confirm to remove tracks.',
            'status': 'Run',
            'message': ''
        })
        if not tracks:
            m = 'There is no tracks to remove on you playlist'
            logger_con.warning(m)
            logger_pro.warning({
                'action': 'Confirm to remove tracks.',
                'status': 'Warning',
                'message': m
            })
            return False

        # Show tracks
        for i, t in enumerate(tracks, start = 1):
            logger_pro.debug(f'Track: [{i}] {t.name}')
            logger_con.debug(f'Track: [{i}] {t.name}')

        while True:
            # Confirm to remove
            q = 'Do you want to remove these tracks from playlist? (y/n): '
            user_input = input(q)
            if helper.is_yes(user_input):
                logger_pro.debug({
                    'action': 'Confirm to remove tracks.',
                    'status': 'Success',
                    'message': '',
                    'user_input': user_input
                })
                return True
            elif helper.is_no(user_input):
                logger_pro.debug({
                    'action': 'Confirm to remove tracks.',
                    'status': 'Success',
                    'message': '',
                    'user_input': user_input
                })
                return False
            else:
                logger_pro.warning({
                    'action': 'Confirm to remove tracks.',
                    'status': 'Warning',
                    'message': '',
                    'user_input': user_input
                })
                continue

    @classmethod
    def extract_track_dict_from_json(cls, track_json: list) -> dict:
        """ 
            Extract track data from tracks json data.

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
            return None
        return track

    @classmethod
    def put_playlist_data_into_tracks_dict(cls, playlist_id: str, tracks_dict: list) -> list:
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
        logger_pro.debug({
            'action': 'Put playlist name and url to tracks dict',
            'status': 'Run',
            'message': ''
        })
        try:
            p_name = NewTrackService.fetch_playlist_name(playlist_id)
            p_url = NewTrackService.fetch_playlist_url(playlist_id)
            for t in tracks_dict:
                t['playlist_name'] = p_name
                t['playlist_url'] = p_url
            logger_pro.debug({
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
        return tracks_dict

    @classmethod
    def retrieve_unique_and_duplicate_tracks_dict(cls, tracks: list, from_tracks: list) -> list:
        """
            Retrieve unique and duplicate tracks dict from tracks dict

            Parameters
            ----------
            tracks: list
                A tracks list to confirm It's unique or no.
            from_tracks: list
                A tracks list to confirm from.

            Raises
            ------
            Warning
                If there is no tracks.
                If there is no from_tracks.
            Exception
                If it fail to retrieve

            Return
            ------
            unique_tracks: list
                An unique track dict list.
            duplicate_tracks: list
                A duplicate track dict list.
        """
        logger_pro.debug({
            'action': 'Retrieve unique and duplicate tracks dict from tracks dict',
            'status': 'Run',
            'message': '',
            'data': {
                'tracks_len': len(tracks),
                'from_tracks_len': len(from_tracks)
            }
        })

        if not tracks:
            logger_pro.warning({
                'action': 'Retrieve unique and duplicate tracks dict from tracks dict',
                'status': 'Warning',
                'message': 'There is no tracks'
            })
            return None, None

        if not from_tracks:
            logger_pro.warning({
                'action': 'Retrieve unique and duplicate tracks dict from tracks dict',
                'status': 'Warning',
                'message': 'There is no from_tracks'
            })
            return None, None      

        unique_tracks = []
        duplicate_tracks = []

        try:
            from_track_urls = [t['track_url'] for t in from_tracks]

            for t in tracks:
                if t['track_url'] in from_track_urls:
                    duplicate_tracks.append(t)
                    logger_pro.debug(f'Duplicate track: {t} by url')
                else:
                    unique_tracks.append(t)
                    logger_pro.debug(f'Unique track: {t} by url')

            logger_pro.debug({
                'action': 'Retrieve unique and duplicate tracks dict from tracks dict',
                'status': 'Success',
                'message': '',
                'data': {
                    'unique_tracks_len': len(unique_tracks),
                    'duplicate_tracks_len': len(duplicate_tracks)
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
        return unique_tracks, duplicate_tracks

    @classmethod
    def retrieve_unique_and_duplicate_tracks(cls, tracks: list, from_tracks: list) -> list:
        """
            Retrieve unique and duplicate new track instances from tracks dict

            Parameters
            ----------
            tracks: list
                A tracks list to confirm It's duplicate or no.
            from_tracks: list
                A tracks list to confirm from.

            Raises
            ------
            Warning
                If there is no tracks.
                If there is no from_tracks.
            Exception
                If it fail to retrieve.

            Return
            ------
            unique_tracks: list
                An unique new tracks instances list.
            duplicate_tracks: list
                A duplicate new tracks instances list.
        """
        logger_pro.info({
            'action': 'Retrieve unique and duplicate new track instances from tracks dict',
            'status': 'Run',
            'message': '',
            'data': {
                'tracks_len': len(tracks),
                'from_tracks_len': len(from_tracks)
            }
        })
        
        if not tracks:
            logger_pro.warning({
                'action': 'Retrieve unique and duplicate new track instances from tracks dict',
                'status': 'Warning',
                'message': 'There is no tracks'
            })
            return None, None

        if not from_tracks:
            logger_pro.warning({
                'action': 'Retrieve unique and duplicate new track instances from tracks dict',
                'status': 'Warning',
                'message': 'There is no from_tracks'
            })
            return None, None

        unique_tracks = []
        duplicate_tracks = []
        try:
            from_track_urls = [t.track_url for t in from_tracks]

            for t in tracks:
                # If url is the same
                if t.track_url in from_track_urls:
                    duplicate_tracks.append(t)
                    logger_pro.debug(f'Duplicate track: {vars(t)} by url')
                else:
                    unique_tracks.append(t)
                    logger_pro.debug(f'Unique track: {vars(t)} by url')
                
            logger_pro.info({
                'action': 'Retrieve unique and duplicate new track instances from tracks dict',
                'status': 'Success',
                'message': '',
                'data': {
                    'unique_tracks_len': len(unique_tracks),
                    'duplicate_tracks_len': len(duplicate_tracks)
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Retrieve unique and duplicate new track instances from tracks dict',
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
        return unique_tracks, duplicate_tracks

    def add_new_tracks(self) -> None:
        """ 
            Add new tracks to csv, gss, spotify playlist
            
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
        
        # Fetch tracks
        tracks_dict_spo = NewTrackService.fetch_tracks_dict_from_playlists()

        # Set tracks
        tracks_spo = []
        for t_dict in tracks_dict_spo:
            t = NewTrackModel()
            t.set_columns(t_dict)
            tracks_spo.append(t)

        # Get tracks on csv
        tracks_csv = csv_repo.all()

        new_tracks, _ = NewTrackService.retrieve_unique_and_duplicate_tracks(tracks_spo, tracks_csv)

        logger_pro.info({
            'action': 'Add new tracks to csv, gss, spotify playlist',
            'status': 'Run',
            'message': ''
        })

        try:
            for t in new_tracks:
                spotify_repo.add(t)
                csv_repo.add(t)
                gss_repo.add(t)
                logger_pro.info({
                    'action': 'Add new tracks to csv, gss, spotify playlist',
                    'status': 'Success',
                    'message': '',
                    'track': vars(t)
                })
        except Exception as e:
            logger_pro.info({
                'action': 'Add new tracks to csv, gss, spotify playlist',
                'status': 'Fail',
                'message': '',
                'track': vars(t)
            })
            raise Exception
        return None

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
        # Fetch playing track
        track_json = NewTrackService.fetch_playing_track_json()
        
        if not track_json:
            message = 'There is no current track you are listening on Spotify right now'
            logger_con.warning(message)
            logger_pro.warning(message)
            return None
        
        # Extrack track dict
        track_json = track_json['item']
        track_dict = NewTrackService.extract_track_dict_from_json(track_json)        

        # Find playing track on csv
        csv_repo = CsvNewTrackRepository()
        track_csv = csv_repo.find_by_url(track_dict['track_url'])

        # Show tracks
        logger_pro.info({
            'action': 'Show current track you are listening.',
            'status': 'Run',
            'message': ''
        })
        if track_csv:
            try:
                logger_con.info(f'Track: {track_csv.name}')  
                logger_con.info(f'Artist: {track_csv.artist}')
                logger_con.info(f'Playlist: {track_csv.playlist_name}')
                logger_pro.info({
                    'action': 'Show current track you are listening.',
                    'status': 'Success',
                    'message': 'Show a playing track with playlist name',
                    'track_csv': vars(track_csv)
                })
            except Exception as e:
                logger_pro.error({
                    'action': 'Show current track you are listening.',
                    'status': 'Fail',
                    'message': 'Show a playing track with playlist name',
                    'exception': e,
                    'track_csv': vars(track_csv)
                })
                raise Exception          
        else:
            try:
                logger_con.info(f'Track: {track_dict["name"]}')  
                logger_con.info(f'Artist: {track_dict["artist"]}')
                logger_pro.info({
                    'action': 'Show current track you are listening.',
                    'status': 'Success',
                    'message': 'Show a playing track without playlist name',
                    'track_dict': track_dict
                })
            except Exception as e:
                logger_pro.error({
                    'action': 'Show current track you are listening.',
                    'status': 'Fail',
                    'message': 'Show a playing track without playlist name',
                    'exception': e,
                    'track_dict': track_dict
                })
                raise Exception
        return None

    def remove_current_tracks(self) -> None:
        """ 
            Remove tracks you listened currently on Spotify.

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
        current_tracks_json = NewTrackService.fetch_current_tracks_json()
        if not current_tracks_json:
            m = 'There is no current tracks. So There is no tracks to remove on your playlist'
            logger_con.warning(m)
            logger_pro.warning(m)
            return None

        # Extract tracks dict from json
        current_tracks_json = current_tracks_json['items']
        current_tracks = []
        for i, t in enumerate(current_tracks_json, start=1):
            #  Extract track dict
            t = t['track']
            track_dict = NewTrackService.extract_track_dict_from_json(t)

            # Set dict data up New Track instance 
            track = NewTrackModel()
            track.set_columns(track_dict)

            # Show track
            logger_con.info(f'Curent Track: [{i}] {track.name}')
            current_tracks.append(track)
        
        spotify_repo = SpotifyNewTrackRepository()

        # Retrieve only current tracks on playlist
        playlist_tracks = spotify_repo.all()
        if not playlist_tracks:
            m = 'There is no playlist tracks. So There is no tracks to remove on your playlist'
            logger_con.warning(m)
            logger_pro.warning(m)
            return None

        # Retrieve duplicate tracks
        _, duplicate_tracks = NewTrackService.retrieve_unique_and_duplicate_tracks(playlist_tracks, current_tracks)
        if not duplicate_tracks:
            m = 'There is no duplicate tracks. So There is no tracks to remove on your playlist'
            logger_con.warning(m)
            logger_pro.warning(m)
            return None

        # Remove tracks from the playlist
        logger_pro.info({
            'action': 'Remove tracks you listened currently on Spotify.',
            'status': 'Run',
            'message': ''
        })

        if NewTrackService.confirm_remove_tracks(duplicate_tracks):
            try:
                for t in duplicate_tracks:
                    spotify_repo.delete_track(t)
                logger_pro.info({
                    'action': 'Remove tracks you listened currently on Spotify.',
                    'status': 'Success',
                    'message': '',
                    'data': {
                        'deleted_tracks_len': len(duplicate_tracks)
                    }
                })
            except Exception as e:
                logger_pro.error({
                    'action': 'Remove tracks you listened currently on Spotify.',
                    'status': 'Fail',
                    'message': '',
                    'exception': e,
                    'data': {
                        'tracks_len': len(duplicate_tracks)
                    }
                })
                raise Exception
        else:
            m = 'It is canceled'
            logger_con.warning(m)
            logger_pro.warning({
                'action': 'Remove tracks you listened currently on Spotify.',
                'status': 'Warning',
                'message': m
            })

        return None

    def remove_tracks_by_index(self, first: int, last: int) -> None:
        """ 
            Remove tracks by index (first, last) you choose.

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
        tracks_all = spotify_repo.all()
        tracks = tracks_all[first-1:last]

        # Remove tracks
        logger_pro.info({
            'action': 'Remove tracks by index (first, last) you choose.',
            'status': 'Run',
            'message': ''
        })
        if NewTrackService.confirm_remove_tracks(tracks):
            try:
                for t in tracks:
                    spotify_repo.delete_track(t)
                logger_pro.info({
                    'action': 'Remove tracks by index (first, last) you choose.',
                    'status': 'Success',
                    'message': '',
                    'data': {
                        'deleted_tracks_len': len(tracks)
                    }
                })
            except Exception as e:
                logger_pro.error({
                    'action': 'Remove tracks by index (first, last) you choose.',
                    'status': 'Fail',
                    'message': '',
                    'exception': e,
                    'data': {
                        'tracks_len': len(tracks)
                    }
                })
                raise Exception
        else:
            logger_pro.warning({
                'action': 'Remove tracks by index (first, last) you choose.',
                'status': 'Warning',
                'message': 'It was canceled.'
            })
        return None
