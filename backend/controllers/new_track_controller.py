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
