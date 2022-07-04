from repositories.CsvRepository import CsvRepository


class CsvService(object):
    @staticmethod
    def is_not_columns(path: str) -> bool:
        if not CsvRepository.get_header(path):
            return True
        else:
            return False


    @staticmethod
    def get_tracks(csv) -> list:
        if CsvService.is_not_columns(csv.file_path):
            return []

        data = CsvRepository.get_data(csv.file_path)
        return data


    @staticmethod
    def get_header_and_tracks(csv) -> list:
        if CsvService.is_not_columns(csv.file_path):
            return [],[]

        header, data = CsvRepository.get_header_and_data(csv.file_path)
        return header, data    


    @staticmethod
    def add_tracks(csv, tracks: list, country_name: str) -> None:
        if CsvService.is_not_columns(csv.file_path):
            CsvRepository.add_columns(csv.file_path, csv.columns)

        CsvRepository.add(csv.file_path, csv.columns, tracks)
        CsvRepository.add(csv.file_path, csv.columns, tracks)
        return
