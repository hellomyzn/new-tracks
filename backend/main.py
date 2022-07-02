# import controllers.conversation
import os
import spotipy

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

def sort_data(tracks):
    
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
                        'added_at':     added_at[i]}
                        )
    for i in range(num_tracks):
        print(tracks[i] , "\n")



# def main():
    # controller.conversation.talk_about_input_vocabulary()

if __name__ == "__main__":
    spotify = setting()
    playlist_id_ph = "37i9dQZEVXbNBz9cRCSFkY"
    tracks_ph = get_tracks_from_playlist(playlist_id_ph)
    sort_data(tracks_ph)

    # main()