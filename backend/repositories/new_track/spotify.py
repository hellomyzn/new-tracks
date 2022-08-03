import logging

from models.spotify import SpotifyModel
from models.new_track import NewTrackModel
from repositories.new_track.interfaces.new_track_repository import NewTrackRepoInterface
import utils.setting as setting
import utils.helper as helper

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')

class SpotifyNewTrackRepository(NewTrackRepoInterface):
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
        self.spotify = SpotifyModel()
        sheet_name = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_NAME']
        if setting.ENV == 'dev':
            self.playlist_id = setting.CONFIG['PLAYLIST_ID']['TEST']
        else:
            self.playlist_id = setting.CONFIG['PLAYLIST_ID']['NEW_TRACKS']
        

    def all(self) -> list:
        """ 
            Get all tracks on the playlist.
            
            Parameters
            ----------
            None.

            Raises
            ------
            Exception
                If you can not get all tracks from palylist.

            Return
            ------
            tracks: list
                A list of New Tracks
        """
        logger_pro.info({
            'action': f'Get all tracks on the playlist.',
            'status': 'Run',
            'message': ''
        })
        tracks = []
        try:
            tracks_json = self.fetch_tracks_json_from_playlist()
            for t in tracks_json:
                # Extract track dict
                track_json = t['track']
                track_dict = self.extract_track_dict_from_json(track_json)
                
                # Create new track instance
                track = NewTrackModel()
                track.set_columns(track_dict)

                # Add track
                tracks.append(track)
          
            logger_pro.info({
                'action': f'Get all tracks on the playlist.',
                'status': 'Success',
                'message': '',
                'data': {
                    'tracks_len': len(tracks)
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': f'Get all tracks on the playlist.',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'playlist_id': self.playlist_id
                }
            })
            raise Exception

        return tracks

    def fetch_tracks_json_from_playlist(self) -> list:
        """ 
            Fetch tracks json data from a playlist.
            
            Parameters
            ----------
            None.

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
            'action': f'Fetch tracks json data from a playlist ({self.playlist_id}).',
            'status': 'Run',
            'message': ''
        })


        try:
            tracks_number = self.fetch_playlist_track_number()
            max_number = 100
            tracks_json = []
            while max_number < tracks_number:
                offset = len(tracks_json)
                playlist_items = self.spotify.conn.playlist_items(self.playlist_id, limit=100, offset=offset)
                current_tracks_json = playlist_items['items']
                tracks_json += current_tracks_json
                tracks_number -= len(current_tracks_json)
                logger_pro.debug({
                    'action': f'Fetch tracks json data from a playlist ({self.playlist_id}).',
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
                playlist_items = self.spotify.conn.playlist_items(self.playlist_id, limit=100, offset=offset)
                current_tracks_json = playlist_items['items']
                tracks_json += current_tracks_json
                logger_pro.debug({
                    'action': f'Fetch tracks json data from a playlist ({self.playlist_id}).',
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
                'action': f'Fetch tracks json data from a playlist ({self.playlist_id}).',
                'status': 'Fail',
                'message': 'This is in a while loop',
                'exception': e,
                'data': {
                    'playlist_id': self.playlist_id
                }
            })
            raise Exception

        return tracks_json

    def fetch_playlist_track_number(self) -> int:
        """
            Fetch a playlist track number.

            Parameters
            ----------
            None.

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
            'action': f'Fetch a playlist track number. ({self.playlist_id}) ',
            'status': 'Run',
            'message': ''
        })
        try:
            playlist_data = self.spotify.conn.playlist(self.playlist_id)
            track_number = playlist_data['tracks']['total']
            logger_pro.debug({
                'action': f'Fetch a playlist track number. ({self.playlist_id}) ',
                'status': 'Success',
                'message': '',
                'data': {
                    'track_number': track_number
                }
            })
            return track_number
        except Exception as e:
            logger_pro.error({
                'action': f'Fetch a playlist track number. ({self.playlist_id}) ',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'data': {
                    'playlist_id': self.playlist_id
                }
            })
            raise Exception

    def extract_track_dict_from_json(self, track_json: list) -> dict:
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

    def find_by_name_and_artist(self, name: str, artist: str) -> NewTrackModel:
        return
    
    def add(self, track: NewTrackModel) -> None:
        url = [track.track_url]
        
        self.add_tracks_to_playlist(url)
        return
    
    def delete_by_name_and_artist(self, name: str, artist: str) -> None:
        return

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

    def delete_track(self, track: NewTrackModel) -> None:
        """ 
            Delete a track.

            Parameters
            ----------
            track: NewTrackModel
                A new track instance to delete.
            
            Raises
            ------
            Exception
                If you can not delete.

            Return
            ------
            None
        """
        logger_pro.debug({
            'action': 'Delete tracks.',
            'status': 'Run',
            'message': ''
        })
        try:
            url = [track.track_url]
            self.spotify.conn.playlist_remove_all_occurrences_of_items(self.playlist_id, url)
            logger_pro.debug({
                'action': 'Delete tracks.',
                'status': 'Success',
                'message': '',
                'data': {
                    'track': vars(track)
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Delete tracks.',
                'status': 'Fail',
                'message': '',
                'exception': e,
                'args': {
                    'playlist_id': self.playlist_id,
                    'track': vars(track)
                }
            })
            raise Exception
        return None

    def add_tracks_to_playlist(self, urls_list: list) -> None:
        """ Add tracks to a playlist.

        Parameters
        ----------
        urls_list: list
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
                'length': len(urls_list),
                'urls_list': urls_list,
                'playlist_id': self.playlist_id
            }
        })
        try:
            self.spotify.conn.playlist_add_items(self.playlist_id, urls_list, position=0)
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
                'exception': e,
                'data': {
                    'playlist_id': self.playlist_id,
                    'urls_list': urls_list
                }
            })
        return
