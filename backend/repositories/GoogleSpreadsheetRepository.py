import logging
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import utils.setting as setting


logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')


class GoogleSpreadsheetRepository(object):
    """
    A class used to represent a Google Spreadsheet repository.

    Attributes
    ----------
    model:
        A Google Spreadsheet model
    columns: list
        Columns set up on model
    worksheet:
        An instance to connect Google Spreadsheet
    sleep_time_sec: float
        The sleep time by second for the interval 
        to write on a Google Spreadsheet.

    Methods
    ------
    """
    def __init__(self, model):
        """
        Parameters
        ----------
        model:
            A Google Spreadsheet model
        """
        self.model = model
        self.columns = model.columns
        self.worksheet = GoogleSpreadsheetRepository.connect(self.model)
        self.sleep_time_sec = 0.8

    @classmethod
    def connect(cls, model):
        """ Connect Google Spreadsheet.

        Parameters
        ----------
        model:
            A model to connect

        Raises
        ------
        Exception
            If it fails to connect.

        Return
        ------
        worksheet:
            the worksheet to be written
        """
        json_path = setting.AUTHENTICATION_JSON
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        key = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_KEY']

        logger_con.info('Start connecting Google Spreadsheet...')
        logger_pro.info({
            'action': 'Connect Google Spreadsheet',
            'status': 'Run',
            'message': '',
            'data': {
                'json_path': json_path,
                'scope': scope,
                'key': key,
                'sheet_name': model.sheet
            }
        })
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
            gc = gspread.authorize(credentials)
            workbook = gc.open_by_key(key)
            worksheet = workbook.worksheet(model.sheet)

            logger_con.info('Succeed in connecting Google Spreadshee...')
            logger_pro.info({
                'action': 'Connect Google Spreadsheet',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_con.error('Fail to connecting Google Spreadshee...')
            logger_pro.error({
                'action': 'Connect Google Spreadsheet',
                'status': 'Fail',
                'message': e
            })
        return worksheet

    def has_header(self) -> bool:
        """ Confirm there is header on GSS

        Parameters
        ----------
        None

        Raises
        ------
        Exception
            If it fails to connect.

        Return
        ------
        True or False:
            There is header or no.
        """
        header = self.worksheet.row_values(1)
        if header == self.columns:
            return True
        else:
            return False

    def add_header(self) -> None:
        """ Add header

        Parameters
        ----------
        None

        Raises
        ------
        Exception
            If it fails to add.

        Return
        ------
        None
        """
        logger_pro.info({
            'action': 'Add header',
            'status': 'Run',
            'message': '',
        })
        try:
            for i, column in enumerate(self.columns, start=1):
                self.worksheet.update_cell(1, i, column)
            logger_pro.info({
                'action': 'Add header',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Add header',
                'status': 'Fail',
                'message': e
            })
        
        return None

    def add_track(self, track: dict) -> None:
        """ Add a track on CSV

        Parameters
        ----------
        track: dict
            A dict to be add on GSS

        Raises
        ------
        Exception
            If it fails to add a track.

        Return
        ------
        None
        """
        # If the spreadsheet is empty, Add column on header(from (1,1))
        if not self.has_header():
            self.add_header()

        logger_pro.info({
            'action': 'Add a track',
            'status': 'Run',
            'message': '',
            'args': {
                'track': track
            }
        })
        
        row_num = self.find_next_available_row()
        
        for col_num, column in enumerate(self.columns, start=1):
            try:
                self.worksheet.update_cell(row_num,
                                           col_num,
                                           track[column])
                logger_con.info(f'{column}: {track[column]}')
                time.sleep(self.sleep_time_sec)
            except Exception as e:
                logger_pro.error({
                    'action': 'Add a track',
                    'status': 'Fail',
                    'message': e,
                    'data': {
                        'row_num': row_num,
                        'col_num': col_num,
                        'column': column,
                        'track': track
                    }
                })

        logger_pro.info({
            'action': 'Add a track',
            'status': 'Success',
            'message': ''
        })
        return
    
    def find_next_available_row(self) -> int:
        """ Find a next available row on GSS
        This is for confirming from which row is available
        when you add data on GSS.

        Parameters
        ----------
        None

        Raises
        ------
        Exception
            If it fails to find an available row.

        Return
        ------
        available_row: int
            The number of next available row number.
        """
        # it is a list which contains all data on first column
        fist_column_data = list(filter(None, self.worksheet.col_values(1)))
        available_row = int(len(fist_column_data)) + 1
        return available_row
