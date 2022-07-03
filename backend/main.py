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
        tracks.append({'name':         names[i],
                        'url':          urls[i],
                        'artist':       artists[i],
                        'release_date': release_date[i],
                        'added_at':     added_at[i],
                        'created_at':   datetime.datetime.now()}
                        )
    return tracks

def create_columns_csv(url, columns):
    
    print('Create header on CSV')
    # TODO: Get this url from config.ini
    with open(url, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

def is_not_columns(url):
    with open(url, 'r', newline='') as csvfile:
        data = csvfile.readline()
        if not data:
            return True
        else:
            return False

def write_csv(tracks, url, columns):
    if is_not_columns(url):
        create_columns_csv(url, columns)

    with open(url, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        for track in tracks:
            writer.writerow(track)
            print(f"[WRITING]: {track}")






# def main():
    # controller.conversation.talk_about_input_vocabulary()

if __name__ == "__main__":
    columns = ['name', 'artist', 'url', 'release_date', 'added_at', 'created_at']
    csv_url = './src/csv/tracks.csv'
    spotify = setting()
    playlist_id_ph = "37i9dQZEVXbNBz9cRCSFkY"
    tracks_ph = get_tracks_from_playlist(playlist_id_ph)
    tracks_ph = sort_data(tracks_ph)
    write_csv(tracks_ph, csv_url, columns)

    # main()