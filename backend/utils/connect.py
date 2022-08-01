from models.spotify import SpotifyModel


def set_up():
    spotify = SpotifyModel()
    spotify.connect()