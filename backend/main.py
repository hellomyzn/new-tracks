"""Entory point"""
import logging

from utils.logger import SetUpLogging
from controllers.track_controller import TrackController



def main():
    """
        This is entry point
    """
    # TODO: Create command for choise
    
    # Init logger
    SetUpLogging().setup_logging("config/logging_config.yaml")
    track_controller = TrackController()

    logger = logging.getLogger('production')
    # track_controller.add_new_tracks_to_playlist()
    # track_controller.remove_tracks_from_playlist()
    track_controller.show_current_track_from_csv()
    
    # logger = logging.getLogger(__name__)
    # logger.critical('critical')
    logger.warning('warning')
    logger.info(f'App started in {__name__}')
    # logger.info('info')
    # logging.debug('debug')
    # logger.error({
    #     'action': 'create',
    #     'status': 'fail',
    #     'message': 'Api call is failed'
    # })

    # a = 2
    # b = 0

    # try:
    #     hoge = a / b
    # except Exception as e:
    #     logging.critical('Exception occured: ', exc_info=True)


if __name__ == "__main__":
    main()
