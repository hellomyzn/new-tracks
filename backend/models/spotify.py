import setting
import spotipy

class Spotify(object):
    def __init__(self, playlist_name, playlist_id):
        self.connect        = Spotify.connect()
        self.playlist_id    = playlist_id
        self.playlist_name  = playlist_name
        self.playlist_url   = 'https://open.spotify.com/playlist/' + playlist_id
        self.playlist_data  = None
        self.tracks         = []
        self.new_tracks     = []
    
    @classmethod
    def connect(cls):
        # get api data from environment environment variables
        client_id = setting.CONFIG['SPOTIPY']['SPOTIPY_CLIENT_ID']
        client_secret = setting.CONFIG['SPOTIPY']['SPOTIPY_CLIENT_SECRET']

        client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return spotify


