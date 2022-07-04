import abc

class Table(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @classmethod
    def get_columns(cls):
        columns = [
            'name', 
            'artist', 
            'url', 
            'release_date', 
            'added_at', 
            'created_at',
            'like'
            ]
        return columns