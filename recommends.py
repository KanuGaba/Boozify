#coding: utf-8
import json
# Spotify library.
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# URL conversions.
import urllib.request
import bs4
# Youtube stuff.
import youtube

""" Query is the search term, type is the type of search from artist, songname, or genre"""
def searchRecommendations(query, type):
    """
    Set up credentials and authentication
    """
    sp = #spotipy.Spotify(credentials manager)
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

    