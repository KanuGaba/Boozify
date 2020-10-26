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

def getTracksFromSeed(seed, seedType):
    # Creating and authenticating our Spotify app.
    client_credentials_manager = SpotifyClientCredentials(APIs["spotify"]["client_id"], APIs["spotify"]["client_secret"])
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    if seedType == "genre":
        if seed in spotify.recommendation_genre_seeds()['genres']:
            results = spotify.recommendations(seed_genres=[seed], limit=60)
    elif seedType == "artist":
        search = spotify.search(q='artist:' + seed, type='artist')
        items = search['artists']['items']
        if len(items) > 0:
            artist = items[0]
            # need to check that artist['url'] works
            results = spotify.recommendations(seed_artists=[artist['external_urls']['spotify']], limit=60)
    # elif seedType == "song":
    #     results = spotify.search(q='name:' + seed, type='track')
    #     items = results['tracks']['items']
    #     if len(items) > 0:
    #         track = items[0]
    #         return spotify.recommendations(seed_tracks=[track['url']], limit=60)
    trackList = []
    # For each track in the playlist.
    for i in results["tracks"]: # IF SEED, THEN restults["tracks"]
        # In case there's only one artist.
        if (i["artists"].__len__() == 1): # IF SEED, THEN i["artists"]
            # We add trackName - artist.
            trackList.append(i["name"] + " - " + i["artists"][0]["name"]) # IF SEED, THEN i["name"]
        # In case there's more than one artist.
        else:
            nameString = ""
            # For each artist in the track.
            for index, b in enumerate(i["artists"]):
                nameString += (b["name"])
                # If it isn't the last artist.
                if (i["artists"].__len__() - 1 != index):
                    nameString += ", "
            # Adding the track to the list.
            trackList.append(i["name"] + " - " + nameString)

    return trackList

def getTracksFromPlaylist(playlistURL):
    # Creating and authenticating our Spotify app.
    client_credentials_manager = SpotifyClientCredentials(APIs["spotify"]["client_id"], APIs["spotify"]["client_secret"])
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Getting a playlist.
    results = spotify.user_playlist_tracks(user="",playlist_id=playlistURL)

    trackList = []
    # For each track in the playlist.
    for i in results["items"]: # IF SEED, THEN restults["tracks"]
        # In case there's only one artist.
        if (i["track"]["artists"].__len__() == 1): # IF SEED, THEN i["artists"]
            # We add trackName - artist.
            trackList.append(i["track"]["name"] + " - " + i["track"]["artists"][0]["name"]) # IF SEED, THEN i["name"]
        # In case there's more than one artist.
        else:
            nameString = ""
            # For each artist in the track.
            for index, b in enumerate(i["track"]["artists"]):
                nameString += (b["name"])
                # If it isn't the last artist.
                if (i["track"]["artists"].__len__() - 1 != index):
                    nameString += ", "
            # Adding the track to the list.
            trackList.append(i["track"]["name"] + " - " + nameString)

    return trackList

# def getTracks(results):
#     trackList = []
#     # For each track in the playlist.
#     for i in results["items"]: # IF SEED, THEN restults["tracks"]
#         # In case there's only one artist.
#         if (i["track"]["artists"].__len__() == 1): # IF SEED, THEN i["artists"]
#             # We add trackName - artist.
#             trackList.append(i["track"]["name"] + " - " + i["track"]["artists"][0]["name"]) # IF SEED, THEN i["name"]
#         # In case there's more than one artist.
#         else:
#             nameString = ""
#             # For each artist in the track.
#             for index, b in enumerate(i["track"]["artists"]):
#                 nameString += (b["name"])
#                 # If it isn't the last artist.
#                 if (i["track"]["artists"].__len__() - 1 != index):
#                     nameString += ", "
#             # Adding the track to the list.
#             trackList.append(i["track"]["name"] + " - " + nameString)

#     return trackList

def searchYoutube(songName):
    songName += " Music Video"
    api = youtube.API(client_id=APIs["youtube"]["client_id"],
              client_secret=APIs["youtube"]["client_secret"],
              api_key=APIs["youtube"]["api_key"])
    video = api.get('search', q=songName, maxResults=1, type='video', order='relevance')
    return("https://www.youtube.com/watch?v="+video["items"][0]["id"]["videoId"])

if (__name__ == "__main__"):
    playlistURL = str(input("Insert Spotify playlist URL: "))
    # will have to fix this later idk how we will do the front end stuff with this
    # if playlistURL != "":
    #     tracks = getTracks(getResultsFromPlaylist(playlistURL))
    # else:
    #     seedType = str(input("Select \"genre\", \"artist\", or \"song\": "))
    #     seed = str(input("Insert genre, artist, or song: "))
    #     tracks = getTracks(getResultsFromSeed(seed, seedType))
    if playlistURL != "":
        tracks = getTracksFromPlaylist(playlistURL)
    else:
        seedType = str(input("Select \"genre\", \"artist\", or \"song\": "))
        seed = str(input("Insert genre, artist, or song: "))
        tracks = getTracksFromSeed(seed, seedType)

    print("Searching songs...")
    songs = []
    for i in tracks:
        songs.append(searchYoutube(i))
    print("Search finished!")

    print("URL LIST: ")
    for i in songs:
        print(i)