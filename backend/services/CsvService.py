from repositories.CsvRepository import CsvRepository
import helper


class CsvService(object):
    @staticmethod
    def get_tracks(path: str) -> list:
        if CsvService.is_not_columns(path):
            return []

        data = CsvRepository.get_data(path)
        return data


    @staticmethod
    def get_header_and_tracks(path: str) -> list:
        if CsvService.is_not_columns(path):
            return [],[]

        header, data = CsvRepository.get_header_and_data(path)
        return header, data    
    
    
    @staticmethod
    def is_not_columns(path: str) -> bool:
        if not CsvRepository.get_header(path):
            return True
        else:
            return False


    @staticmethod
    def add_tracks(csv, tracks: list, csv_path_of_tracks_by_key: str) -> None:

        if not helper.is_file(csv_path_of_tracks_by_key):
            helper.create_file(csv_path_of_tracks_by_key)

        if CsvService.is_not_columns(csv.file_path):
            CsvRepository.add_columns(csv.file_path, csv.columns)
        
        if CsvService.is_not_columns(csv_path_of_tracks_by_key):
            CsvRepository.add_columns(csv_path_of_tracks_by_key, csv.columns)    

        CsvRepository.add(csv.file_path, csv.columns, tracks)
        CsvRepository.add(csv_path_of_tracks_by_key, csv.columns, tracks)
        return
