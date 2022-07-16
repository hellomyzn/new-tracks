"""Portable Logger anywhere for import."""
import logging.config
import yaml
import os


class SetUpLogging():
    @staticmethod
    def setup_logging(config_path, default_level=logging.info):
        root_dir = os.path.dirname(os.path.abspath('__file__'))        
        path = os.path.join(root_dir, config_path)
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                logging.captureWarnings(True)
        else:
            logging.basicConfig(level=default_level)