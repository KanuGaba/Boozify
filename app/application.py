#coding: utf-8
import json
import flask
# Spotify library.
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Youtube stuff.
import youtube
from youtube_search import YoutubeSearch

application = flask.Flask(__name__)

# Opening our JSON configuration file (which has our tokens).
with open("config.json", encoding='utf-8-sig') as json_file:
    APIs = json.load(json_file)

def getTracksFromSeed(seed, seedType):
    # Creating and authenticating our Spotify applicationlication.
    client_credentials_manager = SpotifyClientCredentials(APIs["spotify"]["client_id"], APIs["spotify"]["client_secret"])
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    if seedType == "genre":
        if seed in spotify.recommendation_genre_seeds()['genres']:
            results = spotify.recommendations(seed_genres=[seed], limit=3)
    elif seedType == "artist":
        search = spotify.search(q='artist:' + seed, type='artist')
        items = search['artists']['items']
        if len(items) > 0:
            artist = items[0]
            results = spotify.recommendations(seed_artists=[artist['external_urls']['spotify']], limit=3)
    # elif seedType == "song":
    #     results = spotify.search(q='name:' + seed, type='track')
    #     items = results['tracks']['items']
    #     if len(items) > 0:
    #         track = items[0]
    #         return spotify.recommendations(seed_tracks=[track['url']], limit=60)
    trackList = []
    # For each track in the playlist.
    for i in results["tracks"]:
        # In case there's only one artist.
        if (i["artists"].__len__() == 1):
            # We add trackName - artist.
            trackList.append(i["name"] + " - " + i["artists"][0]["name"])
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
    # Creating and authenticating our Spotify application.
    client_credentials_manager = SpotifyClientCredentials(APIs["spotify"]["client_id"], APIs["spotify"]["client_secret"])
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Getting a playlist.
    results = spotify.user_playlist_tracks(user="",playlist_id=playlistURL)

    trackList = []
    # For each track in the playlist.
    for i in results["items"]:
        # In case there's only one artist.
        if (i["track"]["artists"].__len__() == 1):
            # We add trackName - artist.
            trackList.append(i["track"]["name"] + " - " + i["track"]["artists"][0]["name"])
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

def searchYoutube(songName):
    songName += " Music Video"
    #api = youtube.API(client_id=APIs["youtube"]["client_id"],
              #client_secret=APIs["youtube"]["client_secret"],
              #api_key=APIs["youtube"]["api_key"])
    #video = api.get('search', q=songName, maxResults=1, type='video', order='relevance')
    video = YoutubeSearch(songName, max_results=1).to_dict()
    #return video["items"][0]["id"]["videoId"]
    return video[0]["id"]

@application.route('/get-link', methods=['POST', 'GET'])
def getLink():
    context = {}
    songs = []
    link = ""
    if flask.request.method == 'POST':
        data = flask.request.get_json()
        if data['seed'] == "Artist":
            if data['search'] == "Beyonce":
                songs = ["Ob7vObnFUJc", "sQgd6MccwZc", "a9HIaGcBocc"]
            else:
                artist = data['search']
                tracks = getTracksFromSeed(artist, "artist")
                for i in tracks:
                    songs.append(searchYoutube(i))
        elif data['seed'] == "Genre":
            genre = data['search']
            tracks = getTracksFromSeed(genre, "genre")
            for i in tracks:
                songs.append(searchYoutube(i))
        elif data['seed'] == "Playlist":
            playlistURL = data['search']
            tracks = getTracksFromPlaylist(playlistURL)
            for i in tracks:
                songs.append(searchYoutube(i))
            
    return flask.make_response(flask.jsonify({"ids": songs}))

@application.route('/', methods=['POST', 'GET'])
def index():
    return flask.render_template('web.html')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080,debug=True)
    