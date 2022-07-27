import logging

import utils.setting as setting
from utils.logger import SetUpLogging
from controllers.new_track_controller import NewTrackController


logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')

class Console(object):
    def __init__(self):
        pass
    
    def start(self) -> None:
        # Init logger
        SetUpLogging().setup_logging(setting.LOG_CONFIG_PATH)
        logger_pro.info('Start app')
        while True:
            print('[1]: add new tracks')
            print('[2]: show track you are listening now')
            print('[3]: remove tracks')
            print('[4]: quit')
            user_input = input('Input what you want to do: ')
            try:
                user_input = int(user_input)
                logger_pro.info(f'User input is ({user_input})')
                break
            except Exception as e:
                logger_con.warning('Input is not appropriate. Choose appropriate number.\n')
                logger_pro.warning(f"User's input is not appropriate: ({user_input})")
        
        new_track_controller = NewTrackController()
        if user_input == 1:
            new_track_controller.add_new_tracks()
        elif user_input == 2:
            print(2)
        elif user_input == 3:
            print(3)
        logger_pro.info('End app')    
        # track_controller = TrackController()
        # track_controller.add_new_tracks_to_playlist()
        # track_controller.show_current_track_from_csv()
        # track_controller.remove_tracks_from_playlist()
        
        return
        
        