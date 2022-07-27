import utils.setting as setting
from models.interfaces.new_track import NewTrack

class NewTrackModel(NewTrack):
    def __init__(self):
        self.columns = NewTrackModel.get_columns()
        self.my_playlist_id = setting.CONFIG['PLAYLIST_ID']['MY_PLAYLIST']