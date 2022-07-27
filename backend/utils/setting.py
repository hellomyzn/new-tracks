from configparser import ConfigParser

import utils.arguments as arguments

# Set up config as dict
config_file = 'config/config.ini'
CONFIG = ConfigParser()
CONFIG.read(config_file)

# Environment
ENV = CONFIG['APP']['ENV']
arg_env = arguments.get_env()
if arg_env == 'dev':
    ENV = arg_env

# Google Spreadsheet
AUTHENTICATION_JSON = CONFIG['GOOGLE_API']['JSONF_DIR'] + CONFIG['GOOGLE_API']['JSON_FILE']

# CSV
DIR_PATH_OF_CSV = CONFIG['FILES']['DIR_CSV']
FILE_PATH_OF_CSV = CONFIG['FILES']['DIR_CSV'] + CONFIG['FILES']['FILENAME_OF_CSV']
FILE_PATH_OF_CSV_TEST = CONFIG['FILES']['DIR_CSV'] + CONFIG['FILES']['FILENAME_OF_CSV_TEST']

# Log config
LOG_CONFIG_PATH = "config/logging_config.yaml"