import abc


class NewTrack(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_columns(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def set_columns(self):
        raise NotImplementedError()
