import os
import pathlib
import datetime
import logging

logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')

def is_file(path: str) -> bool:
    """ Confirm the path exists

    Parameters
    ----------
    path: str
        A path of CSV

    Raises
    ------
    Warning:
        There is no file on the path

    Return
    ------
    True/False
    """

    logger_pro.info({
        'action': 'Confirm the path exists',
        'status': 'Run',
        'message': '',
        'data': {
            'path': path
        }
    })

    if os.path.isfile(path):
        logger_pro.info({
            'action': 'Confirm the path exists',
            'status': 'Success',
            'message': ''
        })
        return True

    logger_con.warning('There is no file or you set path up wrongly')
    logger_pro.warning({
        'action': 'Confirm the path exists',
        'status': 'Warning',
        'message': 'There is no file on the path',
        'data': {
            'path': path
        }
    })
    return False


def create_file(path: str):
    pathlib.Path(path).touch()


def delete_file(path: str):
    os.remove(path)


def is_yes(user_input):
    if user_input.lower() == 'y' or user_input.lower() == 'yes':
        return True
    return False


def is_no(user_input):
    if user_input.lower() == 'n' or user_input.lower() == 'no':
        return True
    return False


def get_date():
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    date = now.strftime('%Y/%m/%d')
    return date
