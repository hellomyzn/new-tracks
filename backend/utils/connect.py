from models.spotify import SpotifyModel
from models.google_spreadsheet import GoogleSpreadsheet


def set_up():
    spotify = SpotifyModel()
    gss = GoogleSpreadsheet()
    spotify.connect()
    gss.connect()