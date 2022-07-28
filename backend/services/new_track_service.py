import logging
import time

from repositories.new_track.spotify import SpotifyNewTrackRepository
from repositories.new_track.csv import CsvNewTrackRepository
from repositories.new_track.google_spreadsheet import GssNewTrackRepository
import utils.helper as helper

logger_pro = logging.getLogger('production')
logger_con = logging.getLogger('console')

class NewTrackService(object):
    """
    A class used to represent a spotify service.

    Attributes
    ----------
    spotify:
        A spotify new track repository.
    csv:
        A csv new track repository.
    gss:
        A google spreadsheet new track repository.

    Methods
    ------
    """

    def __init__(self):
        """
        Parameters
        ----------
        None
        """
        # self.spotify = SpotifyNewTrackRepository()
        # self.csv = CsvNewTrackRepository()
        # self.gss = GssNewTrackRepository()

    @classmethod
    def show_track_names(cls, tracks) -> None:
        names = [track['name'] for track in tracks]
        print("\n")
        for name in names:
            print(f'\t[TRACK NAME] - {name}')
        return

    @classmethod
    def is_in_track(cls, track: dict, tracks: list) -> bool:
        track = {'name': track['name'], 'artist': track['artist']}
        tracks = [{'name': t['name'], 'artist': t['artist']} for t in tracks]
        if track in tracks:
            return True
        else:
            return False

    def add_new_tracks(self) -> None:
        """ Add new tracks to csv, gss, spotify playlist
        
        Parameters
        ----------
        None

        Raises
        ------
        None

        Return
        ------
        None
        """
        # Fetch tracks from playlists
        start = time.time()
        spotify_repo = SpotifyNewTrackRepository()
        tracks_spotify = spotify_repo.fetch_tracks_from_playlists()
        print(len(tracks_spotify))
        print(time.time() - start)
        print(tracks_spotify[0])
        return

    def add_tracks_to_playlist(self, tracks: list, playlist_id: str) -> None:
        """ Add tracks to a playlist.

        Parameters
        ----------
        tracks: list
            A tracks list to add
        playlist_id: str
            A playlist id to add to 
        
        Raises
        ------
        Exception
            If you can not add tracks to the playlist

        Return
        ------
        None
        """
        if not tracks:
            message = 'There is no new tracks to add to playlist on Spotify this time.'
            logger_con.info(message)
            logger_pro.info(message)
            return

        tracks_number = len(tracks)
        max_number = 100
        logger_pro.info({
            'action': 'Add tracks between certain indexs',
            'status': 'Run',
            'message': '',
            'args': {
                'tracks_number': tracks_number
            }
        })
        while max_number < tracks_number:
            
            extracted_tracks, tracks = tracks[0:int(max_number)], tracks[int(max_number)::]
            track_urls = [t['track_url'] for t in extracted_tracks]

            logger_pro.info({
                'action': 'Add tracks between certain indexs',
                'status': 'Success',
                'message': '',
                'args': {
                    'extracted_tracks': len(extracted_tracks),
                    'remaining_track': len(tracks),
                    'track_urls': len(track_urls)
                }
            })

            self.repository.add_tracks_to_playlist(track_urls)
            tracks_number = len(tracks)
        else:
            track_urls = [t['track_url'] for t in tracks]
            logger_pro.info({
                'action': 'Add tracks between certain indexs',
                'status': 'Success',
                'message': '',
                'args': {
                    'tracks': len(tracks),
                    'track_urls': len(track_urls)
                }
            })
            self.repository.add_tracks_to_playlist(track_urls)
        return

    def fetch_current_track(self) -> list:
        """ Fetch a track data you are listening.

        if there is no track you are listening,
        return empty list.

        Parameters
        ----------
        None
        
        Raises
        ------
        Exception
            If you can not fetch current track.

        Return
        ------
        track: list
            A track you are listening.
        """
        track_json_data = self.repository.fetch_current_track_json_data()
        
        if track_json_data:
            track_json_data = track_json_data['item']
            track = SpotifyService.extract_track_data(track_json_data)
        else:
            track = []
            message = 'There is no current track you are listening on Spotify right now'
            logger_con.warning(message)
            logger_pro.warning(message)
        return track

    @staticmethod
    def remove_all_tracks_from_playlist(spotify, playlist_id) -> None:
        # TODO: Test to remove all tracks from a playlist even thought it's more than 100
        tracks = SpotifyService.retrieve_all_tracks_from_playlist(spotify,
                                                                  playlist_id)

        # TODO: if there are more than 100 tracks
        SpotifyRepository.remove_tracks_from_playlist(spotify,
                                                      playlist_id,
                                                      tracks)
        return

    def remove_tracks_from_playlist(self,
                                    playlist_id: str,
                                    tracks: list,
                                    first,
                                    last) -> None:

        # TODO Manage first and last number is proper
        """
        no:
            -1, -2,
            the number more than the number of tracks in playlist,
            first is bigger than last
        """
        tracks = tracks[first-1:last]

        self.repository.remove_tracks_from_playlist(playlist_id,
                                                            tracks)
        return

    @staticmethod
    def remove_tracks_played_recently_from_playlist(spotify,
                                                    playlist_id: str) -> None:
        tracks = []
        tracks_played_recently = []
        tracks_json_data = SpotifyRepository.get_tracks_played_recently(spotify)
        for track_json_data in tracks_json_data:
            track_json_data = track_json_data['track']
            tracks_played_recently += SpotifyService.retrieve_track_data(track_json_data)

        print('TRACKS PLAYED RECENTLY')
        SpotifyService.show_track_names(tracks_played_recently)
        playlist_tracks = SpotifyService.retrieve_all_tracks_from_playlist(spotify, playlist_id)
        for t in tracks_played_recently:
            if SpotifyService.is_in_track(t, playlist_tracks):
                tracks.append(t)

        SpotifyRepository.remove_tracks_from_playlist(spotify,
                                                      playlist_id,
                                                      tracks)

        return
