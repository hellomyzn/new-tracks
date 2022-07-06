import helper
from services.CsvService import CsvService


class SpotifyService(object):

    # TODO: move some functions to repository

    @classmethod
    def retrieve_track_data_for_columns(cls, track_json_data: dict) -> list:
        track = [{ 'name': track_json_data['name'],
                    'artist': track_json_data['artists'][0]['name'],
                    'playlist_name': None,
                    'track_url': track_json_data['external_urls']['spotify'],
                    'playlist_url': None,
                    'release_date': None,
                    'added_at': None,
                    'created_at': helper.get_date(),
                    'like': False}]

        return track

    @classmethod
    def retrieve_track_data_for_columns_from_playlist(cls, tracks_json_data: dict, playlist_json_data: dict) -> list:
        tracks = []
        # Retrieve certain data from json data
        names =         [ t["track"]["name"] for t in tracks_json_data]
        urls =          [ t["track"]["external_urls"]["spotify"] for t in tracks_json_data]
        artists =       [ t["track"]["artists"][0]['name'] for t in tracks_json_data]
        release_date =  [ t["track"]["album"]["release_date"] for t in tracks_json_data]
        added_at =      [ t["added_at"]for t in tracks_json_data]
        playlist_name = playlist_json_data["name"]
        playlist_url = playlist_json_data['external_urls']['spotify']

        print(f'[IFNO] - Retrieve tracks data from playlist: {playlist_name}')

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
    def retrieve_tracks_from_playlist(spotify, playlist_id) -> list:
        # TODO: there is more than 100 tracks
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
    def retrieve_all_tracks_from_playlist(spotify, playlist_id: str) -> list:
        # TODO: there is more than 100 tracks
        tracks = []

        # Check there are more than 100 tracks in a playlist
        playlist_json_data = spotify.connect.playlist(playlist_id)
        tracks_number = playlist_json_data['tracks']['total']
        max_number = 100
        print(f'\n[INFO] - The number of new tracks to retrieve from a playlist on Spotify is {tracks_number}')
        
        while max_number < tracks_number:
            offset = len(tracks)
            tracks_json_data = spotify.connect.playlist_items(playlist_id, fields=None, limit=100, offset=offset, market=None, additional_types=('track', 'episode'))
            tracks_json_data = tracks_json_data["items"]
            tracks += SpotifyService.retrieve_track_data_for_columns_from_playlist(tracks_json_data, playlist_json_data)
            tracks_number -= len(tracks_json_data)             
        else:
            # after while loop
            offset = len(tracks)
            tracks_json_data = spotify.connect.playlist_items(playlist_id, fields=None, limit=100, offset=offset, market=None, additional_types=('track', 'episode'))
            tracks_json_data = tracks_json_data["items"]
            tracks += SpotifyService.retrieve_track_data_for_columns_from_playlist(tracks_json_data, playlist_json_data)

        return tracks

    @staticmethod
    def retrieve_new_tracks(spotify, tracks, csv_path) -> list:
        tracks_only_name_artist_from_csv = []
        tracks_only_name_artist_from_new = []
        new_tracks = []

        # Check there is track data on csv and if so, get header data and all track data on csv
        header, tracks_from_csv = CsvService.get_header_and_tracks(csv_path)

        # If there is no track data, it regards all tracks as new tracks
        if not tracks_from_csv:
            print(f'[INFO] -    The number of new tracks is {len(tracks)}')
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
    def get_current_track(spotify) -> list:
        track_json_data = spotify.connect.current_user_playing_track()
        track_json_data = track_json_data['item']
        track = SpotifyService.retrieve_track_data_for_columns(track_json_data)
        return track

    
    @staticmethod
    def get_tracks_played_recently(spotify) -> list:
        tracks = []
        tracks_json_data = spotify.connect.current_user_recently_played()
        tracks_json_data = tracks_json_data['items']
        for track_json_data in tracks_json_data:
            track_json_data = track_json_data['track']
            tracks += SpotifyService.retrieve_track_data_for_columns(track_json_data)
        
        return tracks

        
    @staticmethod
    def add_tracks_to_playlist(spotify, tracks, playlist_id) -> None:
        if not tracks:
            print('[INFO] - There is no new tracks to add to playlist on Spotify this time.')
            return
        
        # If there are more than 100 tracks in tracks, you need to avoid exception.
        # TODO: need to care of order tracks if there are more than 100 tracks.
        tracks_number = len(tracks)
        print(f'\n[INFO] - The number of new tracks to add to a playlist on Spotify is {tracks_number}')

        max_number = 99
        while max_number < tracks_number:

            piece_of_tracks, tracks = tracks[0:int(max_number)], tracks[int(max_number)::]
            
            urls = []
            for track in piece_of_tracks:
                urls.append(track['track_url'])

            spotify.connect.playlist_add_items(playlist_id, urls, position=0)

            tracks_number = len(tracks)
        
        urls = []
        for track in tracks:
            urls.append(track['track_url'])

        spotify.connect.playlist_add_items(playlist_id, urls, position=0)
        return 


    @staticmethod
    def remove_specific_tracks_from_playlist(spotify, playlist_id, tracks) -> None:
        # TODO: if there are more than 100 tracks
        items = [track['track_url'] for track in tracks]
        names = [track['name'] for track in tracks]
        print('\n')
        for name in names:
            print(f'\t[TRACK NAME] - {name}')

        user_input = input(f'\nDo you want to remove these tracks above from your playlist? [y/n]: ')
        
        if helper.is_yes(user_input):
            spotify.connect.playlist_remove_all_occurrences_of_items(playlist_id, items)
            print("It's removed")

        else:
            print("It's cancelled")
        return


    @staticmethod
    def remove_all_tracks_from_playlist(spotify, playlist_id) -> None:
        # TODO: Test to remove all tracks from a playlist even thought it's more than 100
        tracks = SpotifyService.retrieve_all_tracks_from_playlist(spotify, playlist_id)
        
        # TODO: if there are more than 100 tracks
        SpotifyService.remove_specific_tracks_from_playlist(spotify, playlist_id, tracks)


    @staticmethod
    def remove_tracks_from_playlist(spotify, playlist_id, first, last) -> None:
        # TODO: if there are more than 100 tracks
        all_tracks = SpotifyService.retrieve_all_tracks_from_playlist(spotify, playlist_id)

        # TODO Manage first and last number is proper
        """
        no: 
            -1, -2, 
            the number more than the number of tracks in playlist, 
            first is bigger than last
        """
        tracks = all_tracks[first-1:last]
        
        SpotifyService.remove_specific_tracks_from_playlist(spotify, playlist_id, tracks)

        