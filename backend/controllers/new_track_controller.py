"""Modules"""
import logging

import utils.setting as setting
import utils.helper as helper
import utils.connect as connect
from services.new_track_service import NewTrackService
from services.liked_track_service import LikedTrackService

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')


class NewTrackController():
    """ New tracks
    """

    def __init__(self, env: str = 'pro'):
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

    def remove_current_tracks(self) -> None:
        connect.set_up_spotify()
        new_track_service = NewTrackService()
        new_track_service.remove_current_tracks()
        return

    def remove_tracks_by_index(self, first, last) -> None:
        f = int(first)
        l = int(last)
        connect.set_up_spotify()
        new_track_service = NewTrackService()
        new_track_service.remove_tracks_by_index(f, l)

        return

    def retreave_liked_tracks(self):
        connect.set_up()
        liked_track_service = LikedTrackService()
        tracks_from_spotify = liked_track_service.retreave_liked_tracks()

        # get all liked tracks from csv
        tracks_from_csv = liked_track_service.get_all_tracks()

        # retreave new liked tracks
        urls = set(track["url"] for track in tracks_from_csv)
        names = set(track["name"] for track in tracks_from_csv)

        common_liked_tracks = []
        unique_liked_tracks = []

        for t in tracks_from_spotify:
            if t["url"] not in urls:
                unique_liked_tracks.append(t)
                continue

            if t["name"] not in names:
                unique_liked_tracks.append(t)
                continue

            common_liked_tracks.append(t)


        # add liked tracks on CSV
        # add liked tracks on GSS
        if unique_liked_tracks:
            unique_liked_tracks.reverse()
            print(f'there is unique_liked_tracks: {len(unique_liked_tracks)}')
            liked_track_service.write_to_csv(unique_liked_tracks)

        # toggle liked track on GSS
        # get track urls you woll download

    def podcasts(self):
        connect.set_up()
        new_track_service = NewTrackService()
        podcasts = new_track_service.fetch_podcasts()


