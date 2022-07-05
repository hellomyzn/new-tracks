import helper
from services.CsvService import CsvService


class SpotifyService(object):

    @staticmethod
    def retrieve_tracks_from_playlist(spotify, playlist_id) -> list:
        tracks = []
        playlist_json_data = spotify.connect.playlist(playlist_id)        
        tracks_json_data = playlist_json_data["tracks"]["items"]

        # Retrieve certain data from json data
        names =         [ t["track"]["name"] for t in tracks_json_data]
        urls =          [ t["track"]["external_urls"]["spotify"] for t in tracks_json_data]
        artists =       [ t["track"]["artists"][0]['name'] for t in tracks_json_data]
        release_date =  [ t["track"]["album"]["release_date"] for t in tracks_json_data]
        added_at =      [ t["added_at"]for t in tracks_json_data]
        playlist_name = playlist_json_data["name"]
        playlist_url = playlist_json_data['external_urls']['spotify']

        print(f'[IFNO] - playlist: {playlist_name}')

        for i in range(len(names)):
            tracks.append({'name': names[i],
                                    'artist': artists[i],
                                    'playlist_name': playlist_name,
                                    'track_url': urls[i],
                                    'playlist_url': playlist_url,
                                    'release_date': release_date[i],
                                    'added_at': added_at[i],
                                    'created_at': helper.get_date(),
                                    'like': False})

        return tracks


    @staticmethod
    def retrieve_new_tracks(spotify, tracks, csv_path) -> None:
        tracks_only_name_artist_from_csv = []
        tracks_only_name_artist_from_new = []
        new_tracks = []

        # Check there is track data on csv and if so, get header data and all track data on csv
        header, tracks_from_csv = CsvService.get_header_and_tracks(csv_path)

        # If there is no track data, it regards all tracks as new tracks
        if not tracks_from_csv:
            return tracks

        # Prepare a list from csv to check which tracks are new for this time
        for track in tracks_from_csv:
            tracks_only_name_artist_from_csv.append({
                'name':     track[header.index('name')],
                'artist':   track[header.index('artist')]})

        # Prepare a list from retrieved tracks to check which tracks are new for this time
        for track in tracks:
            tracks_only_name_artist_from_new.append({
                'name':     track['name'],
                'artist':   track['artist']})
        
        # Check which tracks are new
        for i, track in enumerate(tracks_only_name_artist_from_new):
            if track in tracks_only_name_artist_from_csv:
                continue
            new_tracks.append(tracks[i])

        print(f'[INFO] -    The number of new tracks is {len(new_tracks)}')
        return new_tracks


    @staticmethod
    def add_tracks_to_playlist(spotify, tracks, playlist_id) -> None:
        if not tracks:
            print('[INFO] - There is no new tracks to add to playlist on Spotify this time.')
            return
        
        print(f'\n[INFO] - The number of new tracks to add to a playlist on Spotify is {len(tracks)}')
        urls = []
        for track in tracks:
            urls.append(track['track_url'])

        spotify.connect.playlist_add_items(playlist_id, urls, position=0)        
        return 


    @staticmethod
    def delete_all_tracks_from_playlist(spotify, playlist_id) -> None:
        SpotifyService.get_tracks_from_playlist(playlist_id)
        SpotifyService.retrieve_tracks_data_from_json(spotify)
        items = spotify.connect.playlist_items(playlist_id)
        print(items)
        # spotify.playlist_remove_all_occurrences_of_items(playlist_id, items)
        