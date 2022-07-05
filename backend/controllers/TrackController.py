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
        self.spotify = Spotify()
        self.google_spreadsheet = GoogleSpreadsheet()
        self.all_new_tracks = []
        self.my_playlist_id = setting.MY_PLAYLIST_ID

    def add_new_tracks(self) -> None:
        all_new_tracks = []
        # Add new tracks by each playlist
        for playlist_id in setting.PLAYLISTS_IDS:            
            self.spotify.new_tracks = []

            tracks      = SpotifyService.retrieve_tracks_from_playlist(self.spotify, playlist_id)
            new_tracks  = SpotifyService.retrieve_new_tracks(self.spotify, tracks,  self.csv.file_path)
            
            # Add tracks to CSV            
            CsvService.add_tracks(self.csv, new_tracks)

            # Add new tracks of the playlist to total one
            if new_tracks:
                all_new_tracks += new_tracks        
        
        GoogleSpreadsheetService.add_tracks(self.google_spreadsheet, all_new_tracks)
        SpotifyService.add_tracks_to_playlist(self.spotify, all_new_tracks, self.my_playlist_id)
        # SpotifyService.delete_all_tracks_from_playlist(self.spotify, self.my_playlist_id)
        return 