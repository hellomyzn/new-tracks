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

    def show_current_track(self):
        SpotifyService.get_current_track(self.spotify)

    def add_new_tracks_to_playlist(self) -> None:
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

        return 
    
    def remove_tracks_from_playlist(self) -> None:
        if helper.is_yes(input("\nDo you want to remove some tracks you've already listened from playlist? (y/n): ")):
            SpotifyService.remove_tracks_played_recently_from_playlist(self.spotify, setting.MY_PLAYLIST_ID)
        else:
            print('You can remove tracks between the track number(first) you choose and the track number(last) you choose')
            first = int(input('Enter a track number (first): '))
            last =  int(input('Enter a track number (last): '))
            SpotifyService.remove_tracks_from_playlist(self.spotify, setting.MY_PLAYLIST_ID, first, last)

        return