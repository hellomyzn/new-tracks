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
            logger_con.warning('There is no new tracks to add to Google Spreadsheet this time.')
            logger_pro.warning('There is no new tracks to add to Google Spreadsheet this time.')
            return

        # If the spreadsheet is empty, Add column on header(from (1,1))
        # if GoogleSpreadsheetService.is_not_columns(google_spreadsheet.worksheet):
        #     GoogleSpreadsheetService.create_columns(google_spreadsheet.worksheet, google_spreadsheet.columns)
        #     google_spreadsheet.next_row += 1

        count = 1
        print(f'\n[INFO] - The number of new tracks to add to Google Spreadsheet is {len(tracks)}')

        for track in tracks:
            print(f'\n[{count}/{len(tracks)}]')
            print(f'[TRACK]: {track}')
            row_number = self.repository.next_available_row()
            print(row_number)
            
            for column_number, column in enumerate(self.model.columns, start=1):
                print(column_number,row_number, column )
                self.repository.add(row_number, column_number, column, track)
 
            row_number += 1
            count += 1
        return        

    @classmethod
    def create_columns(cls, worksheet, columns):
        print('Create header on GSS')
        for i, column in enumerate(columns, start=1):
            worksheet.update_cell(1, i, column)

        return None

    @classmethod
    def is_not_columns(cls, worksheet):
        if worksheet.row_values(1) == []:
            return True
        else:
            return False
