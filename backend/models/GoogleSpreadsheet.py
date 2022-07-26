from models.interfaces.table import Table
import utils.setting as setting

class GoogleSpreadsheet(Table):
    """
        Reference:
        - https://qiita.com/164kondo/items/eec4d1d8fd7648217935
        - https://www.cdatablog.jp/entry/2019/04/16/191006
    """
    def __init__(self):
        self.columns = GoogleSpreadsheet.get_columns()
        self.sheet = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_NAME']
        self.auth_json = setting.AUTHENTICATION_JSON
