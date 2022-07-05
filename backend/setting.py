from configparser import ConfigParser

# Set up config as dict
config_file = 'config.ini'
CONFIG = ConfigParser()
CONFIG.read(config_file)

# Google Spreadsheet
AUTHENTICATION_JSON = CONFIG['GOOGLE_API']['JSONF_DIR'] + CONFIG['GOOGLE_API']['JSON_FILE']

DIR_PATH_OF_CSV = CONFIG['FILES']['DIR_CSV']
FILE_PATH_OF_CSV = CONFIG['FILES']['DIR_CSV'] + CONFIG['FILES']['FILENAME_OF_CSV']

PLAYLIST_ID_GLOBAL = CONFIG['PLAYLIST_ID']['GLOBAL']
PLAYLIST_ID_US = CONFIG['PLAYLIST_ID']['US']
PLAYLIST_ID_JP = CONFIG['PLAYLIST_ID']['JP']
PLAYLIST_ID_PH = CONFIG['PLAYLIST_ID']['PH']
PLAYLIST_ID_IN = CONFIG['PLAYLIST_ID']['IN']
PLAYLIST_ID_IT = CONFIG['PLAYLIST_ID']['IT']
PLAYLIST_ID_UK = CONFIG['PLAYLIST_ID']['UK']
PLAYLIST_ID_KR = CONFIG['PLAYLIST_ID']['KR']
PLAYLIST_ID_SP = CONFIG['PLAYLIST_ID']['SP']
PLAYLIST_ID_FR = CONFIG['PLAYLIST_ID']['FR']


PLAYLIST_DATA = [
    {'name': 'GLOBAL', 'id': PLAYLIST_ID_GLOBAL},
    {'name': 'US', 'id': PLAYLIST_ID_US},
    {'name': 'JP', 'id': PLAYLIST_ID_JP},
    {'name': 'PH', 'id': PLAYLIST_ID_PH},
    {'name': 'IN', 'id': PLAYLIST_ID_IN},
    {'name': 'IT', 'id': PLAYLIST_ID_IT},
    {'name': 'UK', 'id': PLAYLIST_ID_UK},
    {'name': 'KR', 'id': PLAYLIST_ID_KR},
    {'name': 'SP', 'id': PLAYLIST_ID_SP},
    {'name': 'FR', 'id': PLAYLIST_ID_FR}
]