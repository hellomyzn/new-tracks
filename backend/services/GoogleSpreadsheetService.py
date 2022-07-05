import gspread

from repositories.GoogleSpreadsheetRepository import GoogleSpreadsheetRepository

class GoogleSpreadsheetService(object):

    @classmethod
    def create_columns(cls, worksheet, columns):
        print('Create header on GSS')
        for i, column in enumerate(columns, start=1):
            worksheet.update_cell(1, i, column)

        return None


    @classmethod
    def is_not_columns(cls, worksheet):
        if worksheet.row_values(1) == []:
            return True
        else:
            return False


    @staticmethod
    def add_tracks(google_spreadsheet, tracks: list) -> None:
        if not tracks:
            print('[INFO] - There is no new tracks to add to Google Spreadsheet this time.')
            return

        # If the spreadsheet is empty, Add column on header(from (1,1))
        if GoogleSpreadsheetService.is_not_columns(google_spreadsheet.worksheet):
            GoogleSpreadsheetService.create_columns(google_spreadsheet.worksheet, google_spreadsheet.columns)
            google_spreadsheet.next_row += 1

        count = 1
        print(f'\n[INFO] - The number of new tracks to add to Google Spreadsheet is {len(tracks)}')

        for track in tracks:
            print(f'\n[{count}/{len(tracks)}]')
            print(f'[TRACK]: {track}')
            for i, column in enumerate(google_spreadsheet.columns, start=1):
                try:
                    GoogleSpreadsheetRepository.add(google_spreadsheet, i, column, track)
                except gspread.exceptions.APIError:
                    print("[WARNING] - Oops! You exceeded for quota metric 'Write requests' and limit 'Write requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:856605576640'\nTry it again later on!")
                    break

            google_spreadsheet.next_row += 1
            count += 1
        
        return
        