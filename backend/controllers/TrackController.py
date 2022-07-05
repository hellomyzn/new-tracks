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

    def add_new_tracks(self) -> None:
        all_new_tracks = []
        # Add new tracks by each playlist
        for playlist_id in setting.PLAYLISTS_IDS:            
            # Retrieve tracks data from playlist
            tracks      = SpotifyService.retrieve_tracks_from_playlist(self.spotify, playlist_id)

            # Retrieve only new tracks
            new_tracks  = SpotifyService.retrieve_new_tracks(self.spotify, tracks,  self.csv.file_path)
            
            # Add tracks to CSV            
            CsvService.add_tracks(self.csv, new_tracks)

            # Add new tracks of the playlist to total one
            if new_tracks:
                all_new_tracks += new_tracks        
        
        # Add tracks to google spreadsheet
        GoogleSpreadsheetService.add_tracks(self.google_spreadsheet, all_new_tracks)

        # Add tracks to a playlist on Spotify
        SpotifyService.add_tracks_to_playlist(self.spotify, all_new_tracks, setting.MY_PLAYLIST_ID)

        # Remove all tracks from playlist 
        # SpotifyService.delete_all_tracks_from_playlist(self.spotify, setting.MY_PLAYLIST_ID)
        return 