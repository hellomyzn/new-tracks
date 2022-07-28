"""Modules"""
import logging

import utils.setting as setting
import utils.helper as helper
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

        new_track_service = NewTrackService()
        new_track_service.add_new_tracks()
        return

    # def add_new_tracks_to_playlist(self) -> None:
    
    #     # Retrieve new tracks
    #     new_tracks = self.csv_service.retrieve_new_tracks(tracks_from_spotify)

    #     # Add tracks to CSV
    #     self.csv_service.write_tracks(new_tracks)
        
    #     # Add tracks to google spreadsheet
    #     self.google_spreadsheet_service.add_tracks(new_tracks)

    #     # Add tracks to a playlist on Spotify
    #     self.spotify_service.add_tracks_to_playlist(new_tracks)

    #     return

    # def show_current_track_from_csv(self) -> None:
    #     track_from_spotify = self.spotify_service.fetch_current_track()
    #     if track_from_spotify:
    #         track = self.csv_service.show_track(track_from_spotify)
    #     return

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
