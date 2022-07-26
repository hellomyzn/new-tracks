import utils.setting as setting
from models.interfaces.table import Table


class Csv(Table):
    def __init__(self):
        self.columns = Csv.get_columns()
        self.path = setting.FILE_PATH_OF_CSV
        self.dir_path = setting.DIR_PATH_OF_CSV
