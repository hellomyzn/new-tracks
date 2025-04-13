import logging

from models.spotify import SpotifyModel
from repositories.licked_track.csv import CsvLikedTrackRepository
from repositories.licked_track.google_spreadsheet import GssLikedTrackRepository
import utils.helper as helper

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')


class LikedTrackService():
    """
        A class used to represent a liked tracks service.

        Attributes
        ----------
        None

        Methods
        ------
    """

    def __init__(self):
        pass

    def retreave_liked_tracks(self) -> list:
        """[TODO:summary]

        [TODO:description]

        Returns:
            [TODO:description]
        """
        try:
            sp = SpotifyModel()
            total = 0
            remaining = 1
            offset = 0
            limit = 50
            tracks = []

            while remaining > 0:
                logger_con.info(f"start: limit: {limit} offset: {offset} remaining: {remaining}")
                data = sp.conn.current_user_saved_tracks(limit=limit, offset=offset)
                if total == 0:
                    total = int(data["total"])
                    remaining = total

                offset += limit
                items = data["items"]
                for item in items:
                    name = item["track"]["name"]
                    artists = item["track"]["album"]["artists"]
                    if len(artists) > 1:
                        artist = []
                        for a in artists:
                            artist.append(a["name"])
                    else:
                        artist = item["track"]["album"]["artists"][0]["name"]
                    url = item["track"]["album"]["external_urls"]["spotify"]
                    release_date = item["track"]["album"]["release_date"]
                    added_at = item["added_at"].split("T")[0]

                    tracks.append({
                        "name": name,
                        "artist": artist,
                        "url": url,
                        "release_date": release_date,
                        "added_at": added_at,
                        'created_at': helper.get_date()
                    })

                logger_con.info("end")
                remaining -= limit

            return tracks

        except Exception as err:
            print(err)
            return []

    def get_all_tracks(self):
        csv_repository = CsvLikedTrackRepository()
        tracks = csv_repository.get_all()
        return tracks

    def write_to_csv(self, tracks: list):
        csv_repository = CsvLikedTrackRepository()
        gss_repo = GssLikedTrackRepository()
        for track in tracks:
            print(track)

            csv_repository.add_track(track)
            gss_repo.add_track(track)
