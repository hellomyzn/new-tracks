import datetime

from services.CsvService import CsvService


class SpotifyService(object):
    
    @staticmethod
    def get_tracks_from_playlist(spotify) -> None:
        playlist_data = spotify.connect.playlist(spotify.playlist_id)
        spotify.playlist_data = playlist_data["tracks"]["items"]

        return


    @staticmethod
    def retrieve_tracks_data_from_json(spotify) -> None:
        
        # Retrieve certain data from json data
        names =         [ t["track"]["name"] for t in spotify.playlist_data]
        urls =          [ t["track"]["external_urls"]["spotify"] for t in spotify.playlist_data]
        artists =       [ t["track"]["artists"][0]['name'] for t in spotify.playlist_data]
        release_date =  [ t["track"]["album"]["release_date"] for t in spotify.playlist_data]
        added_at =      [ t["added_at"]for t in spotify.playlist_data]
        
        num_tracks = len(names)

        for i in range(num_tracks):
            spotify.tracks.append(
                {
                    'name':         names[i],
                    'artist':       artists[i],
                    'url':          urls[i],                        
                    'release_date': release_date[i],
                    'added_at':     added_at[i],
                    'created_at':   datetime.datetime.now()
                }
            )

        return


    @staticmethod
    def remove_existed_track(spotify, csv_path) -> None:
        tracks_only_name_artist_from_csv = []
        tracks_only_name_artist_from_new = []

        # Check there is track data on csv and if so, get header data and all track data on csv
        header, tracks_from_csv = CsvService.get_header_and_tracks(csv_path)
        # If there is no track data, it regards all tracks as new tracks
        if not tracks_from_csv:
            spotify.new_tracks = spotify.tracks
            return 

        # Prepare a list from csv to check which tracks are new for this time
        for track in tracks_from_csv:
            tracks_only_name_artist_from_csv.append(
                {
                    'name':     track[header.index('name')],
                    'artist':   track[header.index('artist')]
                })

        # Prepare a list from retrieved tracks to check which tracks are new for this time
        for track in spotify.tracks:
            tracks_only_name_artist_from_new.append(
                {
                    'name':     track['name'],
                    'artist':   track['artist']
                }
            )
        
        # Check which tracks are new
        for i, track in enumerate(tracks_only_name_artist_from_new):
            if track in tracks_only_name_artist_from_csv:
                continue
            spotify.new_tracks.append(spotify.tracks[i])
        
        return 
        