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
        self.playlist_id = setting.CONFIG['PLAYLIST_ID']['NEW_TRACKS']
        # self.playlist_id = setting.CONFIG['PLAYLIST_ID']['TEST']

    def all(self) -> list:
        logger_pro.info({
            'action': f'Fetch tracks json data from a playlist ({self.playlist_id}).',
            'status': 'Run',
            'message': ''
        })
        playlist_data = self.spotify.conn.playlist(self.playlist_id)
        tracks_number = playlist_data['tracks']['total']

        max_number = 100
        tracks_json = []
        tracks_dict = []

        try:
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
            for t in tracks_json:
                track = self.extract_track_from_json(t['track'])
                tracks_dict.append(track)
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

        return tracks_dict


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
    
    def add(self, data: dict) -> None:
        url = [data['track_url']]
        
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

    def delete_track_by_url(self, url: str) -> None:
        """ 
            Remove tracks by url

            Parameters
            ----------
            url: str
                A url to remove
            
            Raises
            ------
            Exception
                If you can not remove

            Return
            ------
            None
        """
        url = [url]
        logger_pro.debug({
            'action': 'Remove tracks by url',
            'status': 'Run',
            'message': ''
        })
        try:
            self.spotify.conn.playlist_remove_all_occurrences_of_items(self.playlist_id, url)
            logger_pro.debug({
                'action': 'Remove tracks by url',
                'status': 'Success',
                'message': '',
                'data': {
                    'url': url
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Remove tracks by url',
                'status': 'Fail',
                'message': '',
                'args': {
                    'playlist_id': playlist_id,
                    'url': url
                }
            })
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
