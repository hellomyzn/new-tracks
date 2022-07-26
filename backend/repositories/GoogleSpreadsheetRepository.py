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

    def add(self, 
            row_number: int,
            column_number: int,
            column_name: str,
            data: dict) -> None:
        """ Connect Google Spreadsheet.

        Parameters
        ----------
        None

        Raises
        ------
        Exception
            If it fails to connect.

        Return
        ------
        worksheet:
            the worksheet to be written
        """
        
        self.worksheet.update_cell(row_number,
                                 column_number,
                                 data[column_name])
        print(f"[ADD]: {column_name}:", data[column_name])
        time.sleep(self.sleep_time_sec)

        return

    def next_available_row(self) -> int:
        """ Connect Google Spreadsheet.

        Parameters
        ----------
        None

        Raises
        ------
        Exception
            If it fails to connect.

        Return
        ------
        worksheet:
            the worksheet to be written
        """

        str_list = list(filter(None, self.worksheet.col_values(1)))
        return int(len(str_list)+1)

