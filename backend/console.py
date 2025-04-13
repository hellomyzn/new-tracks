import logging

import utils.setting as setting
import utils.helper as helper
from utils.logger import SetUpLogging
from controllers.new_track_controller import NewTrackController


logger_pro = logging.getLogger('production')
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
            print('[4]: add liked tracks')
            print('[5]: podcasts')
            print('[6]: export')
            print('[7]: quit')
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
            new_track_controller.show_current_track_from_csv()
        elif user_input == 3:
            question = "\nDo you want to remove some tracks you've already listened from playlist? (y/n): "
            if helper.is_yes(input(question)):
                new_track_controller.remove_current_tracks()
            else:
                print('You can remove tracks between the track number(first) you choose and the track number(last) you choose')
                first = int(input('Enter a track number (first): '))
                last = int(input('Enter a track number (last): '))
                new_track_controller.remove_tracks_by_index(first, last)
        elif user_input == 4:
            new_track_controller.retreave_liked_tracks()
        elif user_input == 5:
            new_track_controller.podcasts()
        elif user_input == 6:
            pass

        logger_pro.info('End app')
        return
