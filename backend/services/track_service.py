class TrackService(object):
    def __init__(self):
        pass
    
    def distinct_tracks_by(self, tracks: list, by_tracks: list) -> list:
        """ Remove duplicate tracks by 'by_tracks'

        Parameters
        ----------
        tracks: list
            A tracks list to be compared
        by_tracks: list
            A tracks list to be compared tracks with

        Raises
        ------
        TypeError
            If tracks and/or by_tracks are not list.
        Exception
            If it fails to distinc track by by_tracks.

        Return
        ------
        distincted_tracks: list
            A tracks list removed duplicate tracks
        """
        distincted_tracks = []

        print(tracks)
        print(by_tracks)
        return distincted_tracks
