import logging

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from models.singleton import Singleton
import utils.setting as setting

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')

class GoogleSpreadsheet(Singleton):
    """
        Reference:
        - https://qiita.com/164kondo/items/eec4d1d8fd7648217935
        - https://www.cdatablog.jp/entry/2019/04/16/191006
    """
    connect = None

    def __init__(self):
        pass

    def connect(self) -> None:
        """ Connect Google Spreadsheet.

        Parameters
        ----------
        model:
            A model to connect

        Raises
        ------
        Exception
            If it fails to connect.

        Return
        ------
        worksheet:
            the worksheet to be written
        """
        json_path = setting.AUTHENTICATION_JSON
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        

        logger_con.info('Start connecting Google Spreadsheet...')
        logger_pro.info({
            'action': 'Connect Google Spreadsheet',
            'status': 'Run',
            'message': ''
        })
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
            gc = gspread.authorize(credentials)
            self.conn = gc
            logger_con.info('Succeed in connecting Google Spreadshee...')
            logger_pro.info({
                'action': 'Connect Google Spreadsheet',
                'status': 'Success',
                'message': ''
            })
        except Exception as e:
            logger_con.error('Fail to connecting Google Spreadshee...')
            logger_pro.error({
                'action': 'Connect Google Spreadsheet',
                'status': 'Fail',
                'message': e,
                'data': {
                   'json_path': json_path,
                    'scope': scope
                   }
            })
        return None