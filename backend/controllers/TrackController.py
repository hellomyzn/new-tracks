import setting

from models.Spotify import Spotify
from models.Csv import Csv
from services.SpotifyService import SpotifyService
from services.CsvService import CsvService

class TrackController(object):
    def __init__(self):
        self.csv = Csv(setting.FILE_PATH_OF_CSV)

    def add_new_tracks(self):
        spotify_ph = Spotify(setting.PLAYLIST_ID_PH)

        SpotifyService.get_tracks_from_playlist(spotify_ph)
        SpotifyService.retrieve_tracks_data_from_json(spotify_ph)
        SpotifyService.remove_existed_track(spotify_ph, self.csv)
        CsvService.add_tracks(self.csv, spotify_ph.new_tracks)
        
        
        # tracks_ph = get_tracks_from_playlist(playlist_id_ph)
        # tracks_ph = sort_data(tracks_ph)
        # new_tracks = remove_existed_track(tracks_ph, csv_url)
        # write_csv(new_tracks, csv_url, columns)
        # return