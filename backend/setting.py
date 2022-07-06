from configparser import ConfigParser

# Set up config as dict
config_file = 'config.ini'
CONFIG = ConfigParser()
CONFIG.read(config_file)

# Google Spreadsheet
AUTHENTICATION_JSON = CONFIG['GOOGLE_API']['JSONF_DIR'] + CONFIG['GOOGLE_API']['JSON_FILE']

DIR_PATH_OF_CSV = CONFIG['FILES']['DIR_CSV']
FILE_PATH_OF_CSV = CONFIG['FILES']['DIR_CSV'] + CONFIG['FILES']['FILENAME_OF_CSV']


MY_PLAYLIST_ID = CONFIG['PLAYLIST_ID']['MY_PLAYLIST']


PLAYLISTS_IDS = [
    "37i9dQZEVXbMDoHDwVN2tF", # GLOBAL
    "37i9dQZEVXbLRQDuF5jeBp", # US
    "37i9dQZEVXbKXQ4mDTEBXq", # JP
    "37i9dQZEVXbNBz9cRCSFkY", # PH
    "37i9dQZEVXbLZ52XmnySJg", # IN
    "37i9dQZEVXbLnolsZ8PSNw", # UK
    "37i9dQZEVXbNxXF4SkHj9F", # KR
    "37i9dQZEVXbNFJfN1Vw8d9", # SP
    "37i9dQZEVXbJPcfkRz0wJ0", # AU
    "37i9dQZEVXbJiZcmkrIHGU", # GE
    "37i9dQZEVXbIQnj7RRhdSX", # IT
    "37i9dQZEVXbIPWwFssbupI", # FR
    "37i9dQZEVXbMXbN3EUUhlg", # BR
    "37i9dQZF1DX4JAvHpjipBk"  # New Music Friday
]