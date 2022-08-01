from models.spotify import SpotifyModel
from models.google_spreadsheet import GoogleSpreadsheet


def set_up() -> None:
    spotify = SpotifyModel()
    gss = GoogleSpreadsheet()
    spotify.connect()
    gss.connect()
    return

def set_up_spotify() -> None:
    spotify = SpotifyModel()
    spotify.connect()
    return

def set_up_gss() -> None:
    gss = GoogleSpreadsheet()
    gss.connect()
    return