"""Modules"""
import logging

import utils.setting as setting
import utils.helper as helper
import utils.connect as connect
from services.new_track_service import NewTrackService

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')


class NewTrackController(object):
    def __init__(self, env: str='pro'):
        pass

    def add_new_tracks(self) -> None:
        """ Add new tracks

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
        connect.set_up()
        new_track_service = NewTrackService()
        new_track_service.add_new_tracks()
        return

    def show_current_track_from_csv(self) -> None:
        connect.set_up_spotify()
        new_track_service = NewTrackService()
        new_track_service.show_current_track()
        return

    # def remove_tracks_from_playlist(self) -> None:
    #     my_playlist_id = setting.MY_PLAYLIST_ID
    #     # my_playlist_id = setting.MY_PLAYLIST_ID_TEST
    #     question = "\nDo you want to remove some tracks you've already listened from playlist? (y/n): "
    #     if helper.is_yes(input(question)):
    #         SpotifyService.remove_tracks_played_recently_from_playlist(self.spotify,
    #                                                                    my_playlist_id)
    #     else:
    #         print('You can remove tracks between the track number(first) you choose and the track number(last) you choose')
    #         first = int(input('Enter a track number (first): '))
    #         last = int(input('Enter a track number (last): '))
    #         tracks = self.spotify_service.fetch_tracks_from_playlist(my_playlist_id)
    #         # TODO: remove more than 100 tracks at one time
    #         self.spotify_service.remove_tracks_from_playlist(my_playlist_id,
    #                                                          tracks,
    #                                                          first,
    #                                                          last)
    #     return
