#coding: utf-8
import json
# Spotify library.
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Youtube stuff.
import youtube

# Opening our JSON configuration file (which has our tokens).
with open("config.json", encoding='utf-8-sig') as json_file:
    APIs = json.load(json_file)

def getTracks(playlistURL):
    # Creating and authenticating our Spotify app.
    client_credentials_manager = SpotifyClientCredentials(APIs["spotify"]["client_id"], APIs["spotify"]["client_secret"])
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Getting a playlist.
    results = spotify.user_playlist_tracks(user="",playlist_id=playlistURL)

    trackList = [];
    # For each track in the playlist.
    for i in results["tracks"]["items"]:
        # In case there's only one artist.
        if (i["track"]["artists"].__len__() == 1):
            # We add trackName - artist.
            trackList.append(i["track"]["name"] + " - " + i["track"]["artists"][0]["name"])
        # In case there's more than one artist.
        else:
            nameString = "";
            # For each artist in the track.
            for index, b in enumerate(i["track"]["artists"]):
                nameString += (b["name"]);
                # If it isn't the last artist.
                if (i["track"]["artists"].__len__() - 1 != index):
                    nameString += ", ";
            # Adding the track to the list.
            trackList.append(i["track"]["name"] + " - " + nameString);

    return trackList;

def searchYoutube(songName):
    songName += " Music Video"
    api = youtube.API(client_id=APIs["youtube"]["client_id"],
              client_secret=APIs["youtube"]["client_secret"],
              api_key=APIs["youtube"]["api_key"]);
    video = api.get('search', q=songName, maxResults=1, type='video', order='relevance');
    return("https://www.youtube.com/watch?v="+video["items"][0]["id"]["videoId"]);


""" Query is the search term, type is the type of search from artist, songname, or genre"""
def searchRecommendations(query, type):
    """
    Set up credentials and authentication
    """
      # Creating and authenticating our Spotify app.
    client_credentials_manager = SpotifyClientCredentials(APIs["spotify"]["client_id"], APIs["spotify"]["client_secret"])
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    trackList = [];
    recommended = [];
    # songs are tracks in spotipy
    if (type == "track"):
        result = sp.search(q=query, type=type)
        track_id = result["id"]
        recommended = sp.recommendations(seed_tracks=track_id.tolist(), limit=60)
    else if (type == "artist"):
        result = sp.search(q=query, type=type)
        artist_id = result["id"]
        recommended = sp.recommendations(seed_artists=query.tolist(), limit=60)
    else if (type == "genre"):
        #available gneres to look up can be found in recommendation_genre_seeds
        available_genres = [];
        available_genres = sp.recommendation_genre_seeds()
        if (query in available_genres):
            recommended = sp.recommendations(seed_genres=query, limit=60)
        else:
            #prompt user to pick a new genre, maybe list available genres? 
    
     # For each track in the playlist.
    for i in recommended["tracks"]["items"]:
        # If there is only one artist on a song.
        if (i["track"]["artists"].__len__() == 1):
            # We add trackName - artist music video.
            trackList.append(i["track"]["name"] + " - " + i["track"]["artists"][0]["name"] + " music video")
        # If there are multiple artists on a song
        else:
            nameString = "";
            # For each artist on the track.
            for index, b in enumerate(i["track"]["artists"]):
                nameString += (b["name"]);
                # If it isn't the last artist.
                if (i["track"]["artists"].__len__() - 1 != index):
                    nameString += ", ";
            # Adding the track to the list.
            trackList.append(i["track"]["name"] + " - " + nameString);

    return trackList;

    

if (__name__ == "__main__"):
    tracks = getTracks(str(input("Insert Spotify playlist URL: ")));
    print("Searching songs...");
    songs = [];
    for i in tracks:
        songs.append(searchYoutube(i));
    print("Search finished!");

    print("URL LIST: ");
    for i in songs:
        print(i);