from models.interfaces.table import Table

class Csv(Table):
    def __init__(self, path):
        self.columns = Csv.get_columns()
        self.file_path = path