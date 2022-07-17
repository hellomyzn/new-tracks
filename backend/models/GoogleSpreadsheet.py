from models.interfaces.table import Table


class GoogleSpreadsheet(Table):
    """
        Reference:
        - https://qiita.com/164kondo/items/eec4d1d8fd7648217935
        - https://www.cdatablog.jp/entry/2019/04/16/191006
    """
    def __init__(self):
        self.columns = GoogleSpreadsheet.get_columns()
