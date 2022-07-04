import csv
import os
import datetime

class SpotifyService(object):

    @staticmethod
    def get_tracks_from_playlist(spotify):
        playlist_data = spotify.connect.playlist(spotify.playlist_id)
        spotify.playlist_data = playlist_data["tracks"]["items"]

        return


    @staticmethod
    def retrieve_tracks_data_from_json(spotify) -> list:
        
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
    def remove_existed_track(spotify, path):
        tracks_only_name_artist_from_csv = []
        tracks_only_name_artist_from_new = []

        with open(path, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)
            for row in csvreader:
                tracks_only_name_artist_from_csv.append(
                    {
                        'name':     row[header.index('name')],
                        'artist':   row[header.index('artist')]
                    })

        for track in spotify.tracks:
            tracks_only_name_artist_from_new.append(
                {
                    'name':     track['name'],
                    'artist':   track['artist']
                }
            )
        
        for i, track in enumerate(tracks_only_name_artist_from_new):
            if track in tracks_only_name_artist_from_csv:
                continue
            spotify.new_tracks.append(spotify.tracks[i])
        
        return 
        