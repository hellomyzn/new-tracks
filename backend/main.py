# import controllers.conversation
import os
import datetime
import spotipy
import csv

def setting():
    # get api data from environment environment variables
    client_id = os.environ["SPOTIPY_CLIENT_ID"]
    client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]

    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return spotify

def get_tracks_from_playlist(playlist_id: int):
    playlist = spotify.playlist(playlist_id)
    return playlist["tracks"]["items"]

def sort_data(tracks) -> list:
    
    names =         [ t["track"]["name"] for t in tracks]
    urls =          [ t["track"]["external_urls"]["spotify"] for t in tracks]
    artists =       [ t["track"]["artists"][0]['name'] for t in tracks]
    release_date =  [ t["track"]["album"]["release_date"] for t in tracks]
    added_at =      [ t["added_at"]for t in tracks]
    num_tracks = len(names)
    
    tracks = []

    for i in range(num_tracks):
        tracks.append({'name':          names[i],
                        'artist':       artists[i],
                        'url':          urls[i],                        
                        'release_date': release_date[i],
                        'added_at':     added_at[i],
                        'created_at':   datetime.datetime.now()}
                        )
    return tracks

def remove_existed_track(tracks, url):
    tracks_from_csv = []
    new_tracks_for_check = []
    new_tracks = []
    with open(url, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        for row in csvreader:
            tracks_from_csv.append(
                {
                    'name':     row[header.index('name')],
                    'artist':   row[header.index('artist')]
                })

    for track in tracks:
        new_tracks_for_check.append(
            {
                'name':     track['name'],
                'artist':   track['artist']
            }
        )
    
    for i, track in enumerate(new_tracks_for_check):
        if track in tracks_from_csv:
            continue
        new_tracks.append(tracks[i])
    
    return new_tracks
        





if __name__ == "__main__":
    columns = ['name', 'artist', 'url', 'release_date', 'added_at', 'created_at']
    csv_url = './src/csv/tracks.csv'
    spotify = setting()
    playlist_id_ph = "37i9dQZEVXbNBz9cRCSFkY"
    tracks_ph = get_tracks_from_playlist(playlist_id_ph)
    tracks_ph = sort_data(tracks_ph)
    new_tracks = remove_existed_track(tracks_ph, csv_url)
    write_csv(new_tracks, csv_url, columns)

