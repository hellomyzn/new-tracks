"""Modules"""
import logging

import utils.setting as setting
import utils.helper as helper
from services.CsvService import CsvService
from services.SpotifyService import SpotifyService
from services.GoogleSpreadsheetService import GoogleSpreadsheetService

logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')


class TrackController(object):
    def __init__(self):
        self.csv_service = CsvService()
        self.spotify_service = SpotifyService()    
        self.google_spreadsheet_service = GoogleSpreadsheetService()

    def add_new_tracks_to_playlist(self) -> None:
        # Fetch tracks from playlists
        tracks_from_spotify = self.spotify_service.fetch_tracks_from_playlists(setting.PLAYLISTS_IDS)
        
        # Retrieve new tracks
        new_tracks = self.csv_service.retrieve_new_tracks(tracks_from_spotify)

        # Add tracks to CSV
        self.csv_service.write_tracks(new_tracks)
        
        # Add tracks to google spreadsheet
        self.google_spreadsheet_service.add_tracks(new_tracks)
        return
        # Add tracks to a playlist on Spotify
        self.spotify_service.add_tracks_to_playlist(new_tracks,
                                                    setting.MY_PLAYLIST_ID)

        return

    def show_current_track_from_csv(self) -> None:
        track_from_spotify = self.spotify_service.get_current_track()
        if track_from_spotify:
            track = CsvService.get_track_by_name_and_artist(self.csv.file_path,
                                                            track_from_spotify[0]['name'],
                                                            track_from_spotify[0]['artist'])
            self.csv_service.show_track_info(track)
        return

    def remove_tracks_from_playlist(self) -> None:
        question = "\nDo you want to remove some tracks you've already listened from playlist? (y/n): "
        if helper.is_yes(input(question)):
            SpotifyService.remove_tracks_played_recently_from_playlist(self.spotify,
                                                                       setting.MY_PLAYLIST_ID)
        else:
            print('You can remove tracks between the track number(first) you choose and the track number(last) you choose')
            first = int(input('Enter a track number (first): '))
            last = int(input('Enter a track number (last): '))
            tracks = self.spotify_service.fetch_tracks_from_playlist(setting.MY_PLAYLIST_ID)
            self.spotify_service.remove_tracks_from_playlist(setting.MY_PLAYLIST_ID,
                                                             tracks,
                                                             first,
                                                             last)
        return
