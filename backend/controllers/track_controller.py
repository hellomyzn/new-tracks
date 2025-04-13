"""Modules"""
import logging

import utils.setting as setting
import utils.helper as helper
import utils.connect as connect
from services.new_track_service import NewTrackService
from services.liked_track_service import LikedTrackService

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')


class TrackController():
    """ tracks
    """

    def __init__(self, env: str = 'pro'):
        pass

    def import(self):
        # show playlist (csv)
        # select playlist (csv) 
        # show playlist (spotify)
        # select playlist (spotify) 
            # make a new playlist(spotify)
        # Add CSV
        # Add GSS
        # Add Spotify 
        # Check if it's correct or not
            # Get name, album and artist
        # Show result
        pass

    def export(self):
        pass
