import logging
import time

from models.new_track import NewTrackModel
from models.google_spreadsheet import GoogleSpreadsheet
from repositories.new_track.interfaces.new_track_repository import NewTrackRepoInterface
import utils.setting as setting

import gspread

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')


class GssNewTrackRepository(NewTrackRepoInterface):
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
    def __init__(self):
        """
        Parameters
        ----------
        model:
            A Google Spreadsheet model
        """

        SHEET_SIZE_ERR_STATUS = "INVALID_ARGUMENT"
        REQUEST_LIMIT_ERR_STATUS = "RESOURCE_EXHAUSTED"
        ROW_NUM_TO_ADD = 1000

        key = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_KEY']

        if setting.ENV == 'dev':            
            sheet_name = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_NAME_TEST']
        else:
            sheet_name = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_NAME']

        self.model = NewTrackModel()
        self.columns = self.model.get_columns()
        self.gss = GoogleSpreadsheet()
        self.workbook = self.gss.conn.open_by_key(key)
        self.worksheet = self.workbook.worksheet(sheet_name)
        self.sleep_time_sec = 0.9

    def all(self):
        return


    def find_by_name_and_artist(self, name: str, artist: str):
        return
    

    def add(self, track: NewTrackModel) -> None:
        """ 
            Add a track on GSS

            Parameters
            ----------
            track: NewTrackModel
                A new track instance to add on GSS

            Raises
            ------
            Exception
                If it fails to add a track.

            Return
            ------
            None
        """
        # If the spreadsheet is empty, Add column on header(from (1,1))
        # TODO: move this header validation outside of for statement
        # if not self.has_header():
        #     self.add_header()
        print(self.has_header)

        logger_pro.debug({
            'action': 'Add a track on GSS',
            'status': 'Run',
            'message': '',
            'args': {
                'track': vars(track)
            }
        })

        values = []
        for column in self.columns:
            values.append(getattr(track, column))

        attempts = 1
        max_attempts = 3

        while attempts <= max_attempts:
            try:
                row_num = self.__find_next_available_row()
                self.worksheet.insert_row(values, row_num)
            except ConnectionError as err:
                attempts += 1
                is_connection_err = True
                logger_pro.error({
                    'action': 'Add row',
                    'status': 'Fail: connection error',
                    'message': err
                })
                time.sleep(30)
            except gspread.exceptions.APIError as err:
                err_status = err.response.json()["error"]["status"]
                is_sheet_size_err = bool(err_status == self.SHEET_SIZE_ERR_STATUS)
                is_request_limit = bool(err_status == self.REQUEST_LIMIT_ERR_STATUS)

                if is_sheet_size_err:
                    # no row to add new data in the sheet.
                    # warn("sheet size(row) is not enough. {0}: {1}", err.__class__.__name__, err)
                    time.sleep(10)
                    self.worksheet.add_rows(self.ROW_NUM_TO_ADD)
                    # info("added {0} rows in the sheet({1})", self.ROW_NUM_TO_ADD, self.sheet_name)
                elif is_request_limit:
                    # request quota exceeded the limit
                    # warn("request quota exceeded the limit. {0}: {1}", err.__class__.__name__, err)
                    time.sleep(60)
                else:
                    attempts += 1
                    mes = ("failed to add data into gss 3 times. ",
                           "please check the log. "
                           f"{err.__class__.__name__}: {err}")
                    # error(mes)
                    raise gspread.exceptions.APIError(mes)
            else:
                # success
                # info("added data in the gss({0}).", self.sheet_name)
                is_connection_err = False
                break

        if is_connection_err:
            mes = ("failed to connect to gss 3 times. ",
                   "please check your internet connection.")
            # error(mes)
            raise ConnectionError(mes)

        time.sleep(1)

        
    

    def delete_by_url(self, url: str) -> None:
        pass


    def find_by_url(self, url: str) -> None:
        pass



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

    def __find_next_available_row(self) -> int:
        """ Find a next available row on GSS
            This is for confirming from which row is available
            when you add data on GSS.

        Returns:
            int: _description_
        """
        # it is a list which contains all data on first column
        fist_column_data = list(filter(None, self.worksheet.col_values(1)))
        time.sleep(1)
        available_row = int(len(fist_column_data)) + 1
        return available_row
