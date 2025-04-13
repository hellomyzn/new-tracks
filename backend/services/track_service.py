import logging

from models.spotify import SpotifyModel
from repositories.licked_track.csv import CsvLikedTrackRepository
from repositories.licked_track.google_spreadsheet import GssLikedTrackRepository
import utils.helper as helper

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')


class TrackService():
    """
        A class used to represent a liked tracks service.

        Attributes
        ----------
        None

        Methods
        ------
    """

    def __init__(self):
        pass

