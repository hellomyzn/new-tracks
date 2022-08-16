import logging
import time

from models.new_track import NewTrackModel
from models.google_spreadsheet import GoogleSpreadsheet
from repositories.new_track.interfaces.new_track_repository import NewTrackRepoInterface
import utils.setting as setting

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
        self.sleep_time_sec = 0.8

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
        if not self.has_header():
            self.add_header()

        logger_pro.debug({
            'action': 'Add a track on GSS',
            'status': 'Run',
            'message': '',
            'args': {
                'track': vars(track)
            }
        })
        
        row_num = self.find_next_available_row()
        
        for col_num, column in enumerate(self.columns, start=1):
            try:
                v = getattr(track, column)
                self.worksheet.update_cell(row_num, col_num, v)
                logger_con.debug(f'{column}: {v}')
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
                        'track': vars(track)
                    }
                })
                raise Exception

        logger_pro.debug({
            'action': 'Add a track on GSS',
            'status': 'Success',
            'message': ''
        })
        return None
    

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
