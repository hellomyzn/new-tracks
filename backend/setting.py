from configparser import ConfigParser

# Set up config as dict
config_file = 'config.ini'
CONFIG = ConfigParser()
CONFIG.read(config_file)

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
    {'key': 'GLOBAL', 'id': PLAYLIST_ID_GLOBAL},
    {'key': 'US', 'id': PLAYLIST_ID_US},
    {'key': 'JP', 'id': PLAYLIST_ID_JP},
    {'key': 'PH', 'id': PLAYLIST_ID_PH},
    {'key': 'IN', 'id': PLAYLIST_ID_IN},
    {'key': 'IT', 'id': PLAYLIST_ID_IT},
    {'key': 'UK', 'id': PLAYLIST_ID_UK},
    {'key': 'KR', 'id': PLAYLIST_ID_KR},
    {'key': 'SP', 'id': PLAYLIST_ID_SP},
    {'key': 'FR', 'id': PLAYLIST_ID_FR}
]