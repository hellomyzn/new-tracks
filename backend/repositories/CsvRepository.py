import csv
import logging

logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')

class CsvRepository(object):
    """
    A class used to represent a CSV repository

    Attributes
    ----------
    None
    
    Methods
    ------
    """
    
    def read(self, path: str) -> list:
        tracks = []
        logger_pro.info({
            'action': 'Read tracks data from csv',
            'status': 'Run',
            'message': '',
            'data': {
                'path': path
            }
        })

        try:
            with open(path, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row in csv_reader:
                    tracks.append(row)

            logger_pro.info({
                'action': 'Read tracks data from csv',
                'status': 'Success',
                'message': '',
                'data': {
                    'tracks': tracks
                }
            })
        except Exception as e:          
            logger_pro.warning({
                'action': 'Read tracks data from csv',
                'status': 'Fails',
                'message': '',
                'exception': e
            })

        return tracks

    @staticmethod
    def get_first_data_by_name_and_artist(path: str,
                                          name: str,
                                          artist: str) -> list:
        data = []
        with open(path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                if row[0] == name and row[1] == artist:
                    data = row
                    return data
        return []

    def read_header(self, path: str) -> list:
        """Read header data on CSV

        Parameters
        ----------
        path: str
            The path of CSV

        Raises
        ------
        Exception
            If you fail to read the header.

        Return
        ------
        header: str
            The header on the path of CSV
        """

        logger_pro.info({
            'action': 'Read header data from csv',
            'status': 'Run',
            'message': '',
            'data': {
                'path': path
            }
        })

        try:
            with open(path, 'r', newline='') as csvfile:
                csv_dict_reader = csv.DictReader(csvfile)
                header = csv_dict_reader.fieldnames

            logger_pro.info({
                'action': 'Read header data from csv',
                'status': 'Success',
                'message': '',
                'data': {
                    'header': header
                }
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Read header data from csv',
                'status': 'Fails',
                'message': '',
                'exception': e,
                'data': {
                    'path': path
                }
            })
        if header is None:
            logger_con.warning('There is no header on the CSV')
            logger_pro.warning({
                'action': 'Read header data from csv',
                'status': 'Fails',
                'message': 'There is no header on the CSV',
            })
            
        return header

    @staticmethod
    def get_header_and_data(path: str) -> list:
        data = []
        with open(path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)
            for row in csv_reader:
                data.append(row)

        return header, data

    @staticmethod
    def add_columns(path: str, columns: list) -> None:
        print('[INFO] - Add header on CSV')
        with open(path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()

        return

    def write(self, path: str, columns: list, data: list) -> None:
        logger_pro.info({
            'action': 'Write tracks data on CSV',
            'status': 'Run',
            'message': '',
            'data': {
                'path': path
            }
        })
        try:
            with open(path, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                for d in data:
                    writer.writerow(d)
            logger_pro.info({
                'action': 'Write tracks data on CSV',
                'status': 'Success',
                'message': '',
            })
        except Exception as e:
            logger_pro.warning({
                'action': 'Write tracks data on CSV',
                'status': 'Fails',
                'message': '',
                'exception': e
            })

        return
