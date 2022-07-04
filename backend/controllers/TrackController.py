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
        self.csv_path_of_tracks = self.csv.file_path
        self.csv_path_of_tracks_by_key = None

    def add_new_tracks(self) -> None:
        # Check there is csv file 
        if not helper.is_file(self.csv_path_of_tracks):
            helper.create_file(self.csv_path_of_tracks)
        
        # Add new tracks by each playlist
        for data in setting.PLAYLIST_DATA:
            # CSV path for each playlist
            self.csv_path_of_tracks_by_key = self.csv.dir_path + 'tracks-' + data['key'] + '.csv'
            
            spotify = Spotify(data['id'])      
            SpotifyService.get_tracks_from_playlist(spotify)
            SpotifyService.retrieve_tracks_data_from_json(spotify)
            SpotifyService.remove_existed_track(spotify, self.csv_path_of_tracks)
            CsvService.add_tracks(self.csv, spotify.new_tracks, self.csv_path_of_tracks_by_key)
            GoogleSpreadsheetService.add_tracks(spotify.new_tracks, self.google_spreadsheet)

        return 