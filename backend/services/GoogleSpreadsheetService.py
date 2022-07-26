import gspread
import logging

from models.GoogleSpreadsheet import GoogleSpreadsheet
from models.tests.google_spreadsheet import TestGoogleSpreadsheetModel
from repositories.GoogleSpreadsheetRepository import GoogleSpreadsheetRepository


logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')

class GoogleSpreadsheetService(object):
    """
    A class used to represent a Google Spreadsheet service

    Attributes
    ----------
    model:
        A google spreadsheet model
    repository:
        A google spreadsheet repository

    Methods
    ------
    """
    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        # self.model = GoogleSpreadsheet()
        self.model = TestGoogleSpreadsheetModel()
        self.repository = GoogleSpreadsheetRepository(self.model)

    def add_tracks(self, tracks: list) -> None:
        """ add tracks on Google Spreadsheet

        Parameters
        ----------
        tracks: list
            tracks list data to be add

        Raises
        ------
        Exception
            If it fails to add tracks

        Return
        ------
        None
        """
        if not tracks:
            logger_con.info('There is no new tracks to add to Google Spreadsheet this time.')
            logger_pro.info('There is no new tracks to add to Google Spreadsheet this time.')
            return

        for i, track in enumerate(tracks, start=1):
            logger_con.info(f'[{i}/{len(tracks)}]')
            logger_con.info(f'[TRACK]: {track}')
            self.repository.add_track(track)
        return
