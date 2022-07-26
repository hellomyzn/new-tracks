import utils.setting as setting
from models.interfaces.table import Table


class TestCsvModel(Table):
    def __init__(self):
        self.columns = TestCsvModel.get_columns()
        self.path = setting.FILE_PATH_OF_CSV_TEST
        self.dir_path = setting.DIR_PATH_OF_CSV
