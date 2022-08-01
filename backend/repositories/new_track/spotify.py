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
        self.playlist_id = setting.CONFIG['PLAYLIST_ID']['TEST']

    def all(self) -> list:
        return

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
