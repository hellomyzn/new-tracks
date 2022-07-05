import setting
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os



class Spotify(object):
    def __init__(self):
        self.connect        = Spotify.connect()
        self.tracks         = []
        self.new_tracks     = []
        
    
    @classmethod
    def connect(cls):
        print('[INFO] - Start connecting Spotify...')

        # get api data from environment environment variables
        client_id = setting.CONFIG['SPOTIPY']['SPOTIPY_CLIENT_ID']
        client_secret = setting.CONFIG['SPOTIPY']['SPOTIPY_CLIENT_SECRET']
        redirect_uri = 'http://127.0.0.1:9090'
        scope = 'user-library-read playlist-modify-private'
            
        # client_credentials_manager = SpotifyClientCredentials(client_id=client_id,                                                                 
        #                                                 client_secret=client_secret)
        # spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        auth_manager = SpotifyOAuth(client_id=client_id,
                                    client_secret=client_secret,
                                    redirect_uri=redirect_uri,    
                                    scope=scope,
                                    open_browser=False)

        spotify = spotipy.Spotify(auth_manager=auth_manager)

        return spotify