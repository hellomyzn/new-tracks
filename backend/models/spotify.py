import setting
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os



class Spotify(object):
    def __init__(self):
        self.connect = Spotify.connect()
    
    @classmethod
    def connect(cls):
        print('[INFO] - Start connecting Spotify...')

        # get api data from environment environment variables
        client_id = setting.CONFIG['SPOTIPY']['SPOTIPY_CLIENT_ID']
        client_secret = setting.CONFIG['SPOTIPY']['SPOTIPY_CLIENT_SECRET']
        redirect_uri = 'https://google.com'
        """
            Scope reference:    https://developer.spotify.com/documentation/general/guides/authorization/scopes/
                user-library-read
                playlist-modify-private 
                user-read-recently-played   :    for get playlist information  
                playlist-modify-public      :    for modify public playlist (remove songs from playlist) 
                user-read-currently-playing :    for getting a current track
        """
        scope = 'user-library-read \
                 playlist-modify-private \
                 user-read-recently-played \
                 playlist-modify-public \
                 user-read-currently-playing'
    
        auth_manager = SpotifyOAuth(client_id=client_id,
                                    client_secret=client_secret,
                                    redirect_uri=redirect_uri,    
                                    scope=scope,
                                    open_browser=False)

        spotify = spotipy.Spotify(auth_manager=auth_manager)

        return spotify