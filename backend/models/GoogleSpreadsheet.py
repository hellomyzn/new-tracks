import gspread
from oauth2client.service_account import ServiceAccountCredentials

from models.interfaces.table import Table
import setting


class GoogleSpreadsheet(Table):
    """
        Reference: 
        - https://qiita.com/164kondo/items/eec4d1d8fd7648217935
        - https://www.cdatablog.jp/entry/2019/04/16/191006
    """
    def __init__(self):
        self.columns = GoogleSpreadsheet.get_columns()
        self.worksheet = GoogleSpreadsheet.connect()
        # self.current_vocabularies = self.worksheet.col_values(1)
        self.next_row = GoogleSpreadsheet.next_available_row(self.worksheet)
        self.sleep_time_sec = 0.7

    @classmethod
    def connect(cls):
        print("[INFO] - Start connecting GSS...")
        json_path = setting.AUTHENTICATION_JSON
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        key = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_KEY']
        sheet_name = setting.CONFIG['GOOGLE_API']['Spread_SHEET_NAME']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        gc = gspread.authorize(credentials)
        workbook = gc.open_by_key(key)
        worksheet = workbook.worksheet(sheet_name)
    
        return worksheet
    

    @classmethod
    def next_available_row(cls, worksheet) -> int:
        ''' Return the number of available row '''

        str_list = list(filter(None, worksheet.col_values(1)))
        return int(len(str_list)+1)





    # def update_memorized(self, vocabulary) -> None:
    #     # Update memorized col
    #     cell = self.worksheet.find(vocabulary.title)
    #     self.worksheet.update_cell(cell.row, 8, False)
    #     self.worksheet.update_cell(cell.row, 9, False)
    #     time.sleep(self.sleep_time_sec)
    #     return None