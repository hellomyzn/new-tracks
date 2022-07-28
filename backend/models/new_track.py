import utils.setting as setting
from models.interfaces.new_track import NewTrack

class NewTrackModel(NewTrack):
    def __init__(self):
        self.name = None
        self.artist = None
        self.playlist_name = None
        self.track_url = None
        self.playlist_url = None
        self.added_at = None
        self.created_at = None
        self.like = None
    
    def get_columns(self):
        columns = [
            'name',
            'artist',
            'playlist_name',
            'track_url',
            'playlist_url',
            'release_date',
            'added_at',
            'created_at',
            'like'
            ]
        return columns