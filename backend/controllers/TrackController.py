import setting

import helper
from models.Spotify import Spotify
from models.Csv import Csv
from models.GoogleSpreadsheet import GoogleSpreadsheet
from services.SpotifyService import SpotifyService
from services.CsvService import CsvService
from services.GoogleSpreadsheetService import GoogleSpreadsheetService

class TrackController(object):
    def __init__(self):
        self.csv = Csv()
        self.google_spreadsheet = GoogleSpreadsheet()

    def add_new_tracks(self) -> None:
        # Add new tracks by each playlist
        for playlist_data in setting.PLAYLIST_DATA:
            pl_name = playlist_data['name']
            pl_id = playlist_data['id']
            
            spotify = Spotify(pl_name, pl_id)
            SpotifyService.get_tracks_from_playlist(spotify)        
            SpotifyService.retrieve_tracks_data_from_json(spotify)
            SpotifyService.remove_existed_track(spotify, self.csv.file_path)
            CsvService.add_tracks(self.csv, spotify.new_tracks)
            
        GoogleSpreadsheetService.add_tracks(spotify.new_tracks, self.google_spreadsheet)

        return 