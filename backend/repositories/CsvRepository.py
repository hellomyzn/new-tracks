import csv
import logging

import utils.helper as helper

logger_pro = logging.getLogger('production')
logger_dev = logging.getLogger('develop')
logger_con = logging.getLogger('console')

class CsvRepository(object):
    """
    A class used to represent a CSV repository

    Attributes
    ----------
    path: str
        the csv path
    
    Methods
    ------
    """

    def __init__(self, model):
        """
        Parameters
        ----------
        model:
            A model
        path: str
            A path of csv to manage tracks set up on model
        columns: list
            Columns set up on model
        """
        self.model = model
        self.path = model.path
        self.columns = model.columns
    
    def read_all(self) -> list:
        """ Read all tracks
        
        Parameters
        ----------
        None

        Raises
        ------
        Warning
            if there is no file or you set path up wrongly.
            if there is no any track data in csv file.
        Exception
            If it fails to read tracks

        Return
        ------
        tracks: list
            A list of tracks (each tracks was not dict, just a list)
        """
        tracks = []
        if not helper.exists_file(self.path):
            return []

        if not self.read_header():
            return []

        logger_pro.info({
            'action': 'Read all tracks from csv',
            'status': 'Run',
            'message': '',
            'data': {
                'path': self.path
            }
        })

        try:
            with open(self.path, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row in csv_reader:
                    tracks.append(row)

            logger_pro.info({
                'action': 'Read all tracks from csv',
                'status': 'Success',
                'message': '',
                'data': {
                    'tracks': tracks
                }
            })
        except Exception as e:          
            logger_pro.warning({
                'action': 'Read all tracks from csv',
                'status': 'Fails',
                'message': '',
                'exception': e,
                'data': {
                    'path': self.path
                }
            })

        return tracks

    def read_header(self) -> list:
        """ Read header data on CSV

        Parameters
        ----------
        None

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
                'path': self.path
            }
        })

        try:
            with open(self.path, 'r', newline='') as csvfile:
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
                    'path': self.path
                }
            })
        if header is None:
            logger_pro.warning({
                'action': 'Read header data from csv',
                'status': 'Fails',
                'message': 'There is no header on the CSV',
                'data': {
                    'path': self.path
                }
            })
            
        return header

    def write_header(self) -> None:
        """ Write header on CSV.

        Parameters
        ----------
        tracks: list
            A tracks list to be written on CSV.

        Raises
        ------
        Exception
            If it fails to write on CSV

        Return
        ------
        None
        """
        logger_pro.info({
            'action': 'Write header on CSV.',
            'status': 'Run',
            'message': '',
            'data': {
                'path': self.path,
                'columns': self.columns
            }
        })
        try:
            with open(self.path, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.columns)
                writer.writeheader()

            logger_pro.warning(f'Add header on csv ({self.path})')
            logger_pro.info({
                'action': 'Write header on CSV.',
                'status': 'Success',
                'message': '',
            })
        except Exception as e:
            logger_pro.error({
                'action': 'Write header on CSV.',
                'status': 'Fails',
                'message': '',
                'exception': e
            })

        return

    def write(self, tracks: list) -> None:
        """ Write tracks on CSV.

        If there is no csv file to write,
        create a csv file.

        If there is no header on csv,
        Add headers on csv.

        Parameters
        ----------
        tracks: list
            A tracks list to be written on CSV.

        Raises
        ------
        Exception
            If it fails to write on CSV

        Return
        ------
        None
        """
        # Check there is csv file
        if not helper.exists_file(self.path):
            helper.create_file(self.path)

        # Check there is header
        if self.read_header() is None:
            self.write_header()
    
        with open(self.path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.columns)
            for t in tracks:
                logger_pro.info({
                    'action': 'Write tracks data on CSV',
                    'status': 'Run',
                    'message': '',
                    'data': {
                        'path': self.path,
                        'track': t
                    }
                })
                try:
                    writer.writerow(t)
                    logger_pro.info({
                        'action': 'Write tracks data on CSV',
                        'status': 'Success',
                        'message': ''
                    })
                except Exception as e:
                    logger_pro.error({
                        'action': 'Write tracks data on CSV',
                        'status': 'Fails',
                        'message': '',
                        'exception': e
                    })
        return


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

    @staticmethod
    def get_header_and_data(path: str) -> list:
        data = []
        with open(path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)
            for row in csv_reader:
                data.append(row)

        return header, data
