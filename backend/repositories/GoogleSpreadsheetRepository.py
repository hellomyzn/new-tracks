import logging
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import utils.setting as setting


logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')


class GoogleSpreadsheetRepository(object):
    def __init__(self):
        self.connect = GoogleSpreadsheetRepository.connect()
        self.sleep_time_sec = 0.8

    @classmethod
    def connect(cls):
        print("[INFO] - Start connecting GSS...")
        json_path = setting.AUTHENTICATION_JSON
        print(json_path)
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        key = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_KEY']
        sheet_name = setting.CONFIG['GOOGLE_API']['Spread_SHEET_NAME']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        gc = gspread.authorize(credentials)
        workbook = gc.open_by_key(key)
        worksheet = workbook.worksheet(sheet_name)

        return worksheet

    def next_available_row(self) -> int:
        ''' Return the number of available row '''

        str_list = list(filter(None, self.connect.col_values(1)))
        return int(len(str_list)+1)

    def add(self, 
            row_number: int,
            column_number: int,
            column_name: str,
            data: dict) -> None:
        
        self.connect.update_cell(row_number,
                                 column_number,
                                 data[column_name])
        print(f"[ADD]: {column_name}:", data[column_name])
        time.sleep(self.sleep_time_sec)

        return
