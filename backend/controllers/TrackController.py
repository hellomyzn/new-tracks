import setting

from models.Spotify import Spotify
from models.Csv import Csv
from services.SpotifyService import SpotifyService
from services.CsvService import CsvService

class TrackController(object):
    def __init__(self):
        self.csv = Csv(setting.FILE_PATH_OF_CSV)

    def add_new_tracks(self):
        for country, id in setting.PLAYLIST_IDS:
            spotify = Spotify(id)
            SpotifyService.get_tracks_from_playlist(spotify)
            SpotifyService.retrieve_tracks_data_from_json(spotify)
            SpotifyService.remove_existed_track(spotify, self.csv)
            CsvService.add_tracks(self.csv, spotify.new_tracks)