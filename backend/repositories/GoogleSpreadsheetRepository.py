import time

class GoogleSpreadsheetRepository(object):
    @staticmethod
    def add(google_spreadsheet, column_number, column_name, data: list) -> None:
        google_spreadsheet.worksheet.update_cell(google_spreadsheet.next_row, column_number, data[column_name])
        print(f"[ADD]: {column_name}:", data[column_name])
        time.sleep(google_spreadsheet.sleep_time_sec)

        return