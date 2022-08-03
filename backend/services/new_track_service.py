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
        # Fetch tracks
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
                # Fetch json data
                tracks_json = self.fetch_tracks_json_from_playlist(p_id)
                # Extract only the data we need
                tracks_json = [t['track'] for t in tracks_json]
                # Extract track data
                tracks_dict = [self.extract_track_from_json(t) for t in tracks_json]
                # Remove duplicated tracks amoung the playlists
                tracks_dict = self.retrieve_unique_tracks_dict(tracks_dict, new_tracks_dict)
                # Put playlist data on tracks dict
                tracks_dict = self.put_playlist_data_into_tracks_dict(p_id, tracks_dict)
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
            track = self.extract_track_from_json(track_json)
        else:
            track = []
            message = 'There is no current track you are listening on Spotify right now'
            logger_con.warning(message)
            logger_pro.warning(message)
        return track

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

    def fetch_current_tracks_json(self) -> dict:
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

    def extract_track_from_json(self, track_json: list) -> dict:
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
            raise Exception
        return track

    def put_playlist_data_into_tracks_dict(self, playlist_id: str, tracks_dict: list) -> list:
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
        try:
            p_name = self.fetch_playlist_name(playlist_id)
            p_url = self.fetch_playlist_url(playlist_id)
            for t in tracks_dict:
                t['playlist_name'] = p_name
                t['playlist_url'] = p_url
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
        return tracks_dict

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

    def retrieve_duplicate_tracks_dict(self, tracks: list, from_tracks: list) -> list:
        """
            Retrieve duplicate tracks dict from tracks dict

            Parameters
            ----------
            tracks: list
                A tracks list to confirm It's duplicate or no.
            from_tracks: list
                A tracks list to confirm from.

            Raises
            ------
            Exception
                If it fail to retrieve

            Return
            ------
            duplicate_tracks: list
                a unique tracks list.
        """
        logger_pro.info({
            'action': 'Retrieve duplicate tracks dict from tracks dict',
            'status': 'Run',
            'message': '',
            'data': {
                'tracks_len': len(tracks),
                'from_tracks_len': len(from_tracks)
            }
        })
        
        if not tracks:
            logger_pro.warning({
                'action': 'Retrieve duplicate tracks dict from tracks dict',
                'status': 'Warning',
                'message': 'There is no tracks',
                'data': {
                    'tracks_len': len(tracks)
                }
            })
            return tracks

        duplicate_tracks = []
        try:
            from_track_names = [t['name'] for t in from_tracks]
            from_track_artists = [t['artist'] for t in from_tracks]
            for track in tracks:
                if track['name'] in from_track_names and track['artist'] in from_track_artists:
                    duplicate_tracks.append(track)
                    logger_pro.debug({
                        'action': 'Retrieve duplicate tracks dict from tracks dict',
                        'status': 'Success',
                        'message': '',
                        'data': {
                            'duplicate_tracks': track
                        }
                    })
                continue

            logger_pro.info({
                'action': 'Retrieve duplicate tracks dict from tracks dict',
                'status': 'Success',
                'message': '',
                'data': {
                    'duplicate_tracks_len': len(duplicate_tracks)
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Retrieve duplicate tracks dict from tracks dict',
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
        return duplicate_tracks

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
        tracks_json = self.fetch_current_tracks_json()
        # Extract tracks from json
        tracks_json = tracks_json['items']
        tracks_dict = []
        for i, t in enumerate(tracks_json, start=1):
            t = t['track']
            track_dict = self.extract_track_from_json(t)
            logger_con.info(f'Curent Track: [{i}] {track_dict["name"]}')
            tracks_dict.append(track_dict)
        
        spotify_repo = SpotifyNewTrackRepository()

        # Retrieve only current tracks on playlist
        playlist_tracks_dict = spotify_repo.all()
        duplicate_tracks = self.retrieve_duplicate_tracks_dict(tracks_dict, playlist_tracks_dict)

        if not duplicate_tracks:
            m = 'There is no tracks to remove on you playlist'
            logger_con.warning(m)
            logger_pro.warning(m)
            return None

        # Show duplicate tracks
        for i, t in enumerate(duplicate_tracks, start = 1):
            logger_con.info(f'Duplicate Track: [{i}] {t["name"]}')

        # Confirm to remove
        q = 'Do you want to remove these tracks from playlist? (y/n): '
        user_input = input(q)
        
        # Remove tracks
        if helper.is_yes(user_input):
            for t in duplicate_tracks:
                spotify_repo.delete_track_by_url(t['track_url'])
        else:
            m = 'It is canceled'
            logger_con.warning(m)
            logger_pro.warning(m)
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
    
    