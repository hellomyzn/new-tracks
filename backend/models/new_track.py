import utils.setting as setting
from models.interfaces.new_track import Track

class NewTrackModel(Track):
    def __init__(self, name, artist, playlist_name, 
                 track_url, playlist_url, added_at, 
                 created_at, like):
        self.name = name
        self.artist = artist
        self.playlist_name = playlist_name
        self.track_url = track_url
        self.playlist_url = playlist_url
        self.added_at = added_at
        self.created_at = created_at
        self.like = like
    
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