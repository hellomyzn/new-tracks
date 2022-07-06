import helper

class SpotifyRepository(object):
    
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


    @staticmethod
    def get_current_track(spotify) -> list:
        track_json_data = spotify.connect.current_user_playing_track()
        track_json_data = track_json_data['item']
        track = SpotifyRepository.retrieve_track_data_for_columns(track_json_data)
        return track


    @staticmethod
    def get_tracks_played_recently(spotify) -> list:
        tracks = []
        tracks_json_data = spotify.connect.current_user_recently_played()
        tracks_json_data = tracks_json_data['items']
        for track_json_data in tracks_json_data:
            track_json_data = track_json_data['track']
            tracks += SpotifyRepository.retrieve_track_data_for_columns(track_json_data)
            
        return tracks

    @staticmethod
    def remove_tracks_from_playlist(spotify, playlist_id, tracks) -> None:
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