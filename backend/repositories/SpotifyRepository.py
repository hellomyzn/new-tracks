import utils.helper as helper


class SpotifyRepository(object):
    @staticmethod
    def get_current_track(spotify) -> list:
        track_json_data = spotify.connect.current_user_playing_track()
        try:
            track_json_data = track_json_data['item']
        except TypeError:
            print("[WARNING] - There is no current track you are listening on Spotify right now")
            # logging.critical('Exception occured: ', exc_info=True)
            track_json_data = []

        return track_json_data

    @staticmethod
    def get_tracks_played_recently(spotify) -> list:
        tracks = []
        tracks_json_data = spotify.connect.current_user_recently_played()
        tracks_json_data = tracks_json_data['items']
        return tracks_json_data

    @staticmethod
    def remove_tracks_from_playlist(spotify, playlist_id, tracks) -> None:
        # TODO: if there are more than 100 tracks
        items = [track['track_url'] for track in tracks]
        names = [track['name'] for track in tracks]
        print('\n')
        for name in names:
            print(f'\t[TRACK NAME] - {name}')

        # TODO: If there is no track this time, return and print there is no track this time
        question = '\nDo you want to remove these tracks above from your playlist? [y/n]: '
        user_input = input(question)

        if helper.is_yes(user_input):
            spotify.connect.playlist_remove_all_occurrences_of_items(playlist_id, items)
            print("It's removed")
        else:
            print("It's cancelled")
        return
