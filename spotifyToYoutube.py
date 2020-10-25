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

def getResultsFromSeed(seed, seedType):
    # Creating and authenticating our Spotify app.
    client_credentials_manager = SpotifyClientCredentials(APIs["spotify"]["client_id"], APIs["spotify"]["client_secret"])
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    if seedType == "genre":
        # may need to make this a dropdown and use recommendation_genre_seeds()
        # just gonna assume for now that they know what they're doing
        return recommendations(seed_genre=seed, limit=60)
    elif seedType == "artist":
        results = spotify.search(q='artist:' + seed, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            # need to check that artist['url'] works
            return recommendations(seed_artists=[artist['url']], limit=60)
    elif seedType == "song":
        results = spotify.search(q='name:' + seed, type='track')
        # have to double check results dict
        items = results['tracks']['items']
        if len(items) > 0:
            track = items[0]
            return recommendations(seed_tracks=[track['url']], limit=60)

def getResultsFromPlaylist(playlistURL):
    # Creating and authenticating our Spotify app.
    client_credentials_manager = SpotifyClientCredentials(APIs["spotify"]["client_id"], APIs["spotify"]["client_secret"])
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Getting a playlist.
    return spotify.user_playlist_tracks(user="",playlist_id=playlistURL)

    
def getTracks(results):
    trackList = [];
    # For each track in the playlist.
    for i in results["items"]:
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

if (__name__ == "__main__"):
    playlist = str(input("Insert Spotify playlist URL: "))
    # will have to fix this later idk how we will do the front end stuff with this
    seed = str(input("Insert genre, artist, or song: "))
    seedType = str(input("Insert genre, artist, or song: "))

    if playlist != "":
        tracks = getTracks(getResultsFromPlaylist(playlistURL))
    tracks = getTracks(getResultsFromSeed(seed, seedType))

    print("Searching songs...");
    songs = [];
    for i in tracks:
        songs.append(searchYoutube(i));
    print("Search finished!");

    print("URL LIST: ");
    for i in songs:
        print(i);