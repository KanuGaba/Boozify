#coding: utf-8
import json
import flask
# Spotify library
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Youtube stuff
import youtube
from youtube_search import YoutubeSearch

# Constant vars
NUM_SONGS = 60
NUM_ATTEMPTS = 3 # Could prob remove attempts logic

application = flask.Flask(__name__)

# Opening our JSON configuration file (which has our tokens)
with open("config.json", encoding='utf-8-sig') as json_file:
    APIs = json.load(json_file)

def getTracksFromSeed(seed, seedType):
    # Creating and authenticating our Spotify applicationlication
    client_credentials_manager = SpotifyClientCredentials(APIs["spotify"]["client_id"], APIs["spotify"]["client_secret"])
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    print("Searching Spotify with {} {}".format(seedType, seed))

    trackList = []
    attempts = NUM_ATTEMPTS
    while attempts != 0:
        song_limit = NUM_SONGS - len(trackList)

        # Exit loop if we received NUM_SONGS in the trackList
        if song_limit == 0:
            break

        print("Attempts Left {}".format(attempts - 1))

        # Spotify API to find search results
        if seedType == "genre":
            if seed in spotify.recommendation_genre_seeds()['genres']:
                results = spotify.recommendations(seed_genres=[seed], limit=song_limit)
        elif seedType == "artist":
            search = spotify.search(q='artist:' + seed, type='artist')
            items = search['artists']['items']
            if len(items) > 0:
                artist = items[0]
                results = spotify.recommendations(seed_artists=[artist['external_urls']['spotify']], limit=song_limit)

        for i in results["tracks"]:
            # If there's only one artist add "trackName - artist"
            if (i["artists"].__len__() == 1):
                trackList.append(i["name"] + " - " + i["artists"][0]["name"])
            # Else add "trackName - artist1, artist2, etc"
            else:
                nameString = ""
                for index, b in enumerate(i["artists"]):
                    nameString += (b["name"])
                    if (i["artists"].__len__() - 1 != index):
                        nameString += ", "
                trackList.append(i["name"] + " - " + nameString)

        attempts -= 1

    return trackList

def getTracksFromPlaylist(playlistURL):
    # Creating and authenticating our Spotify application
    client_credentials_manager = SpotifyClientCredentials(APIs["spotify"]["client_id"], APIs["spotify"]["client_secret"])
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    print("Searching Spotify with playlist {}".format(playlistURL))

    # Spotify API to get a playlist
    results = spotify.user_playlist_tracks(user="",playlist_id=playlistURL)

    trackList = []

    for i in results["items"]:
        # Limit playlist to NUM_SONGS
        if len(trackList) == NUM_SONGS:
            break

        # If there's only one artist add "trackName - artist"
        if (i["track"]["artists"].__len__() == 1):
            trackList.append(i["track"]["name"] + " - " + i["track"]["artists"][0]["name"])
        # Else add "trackName - artist1, artist2, etc"
        else:
            nameString = ""
            for index, b in enumerate(i["track"]["artists"]):
                nameString += (b["name"])
                if (i["track"]["artists"].__len__() - 1 != index):
                    nameString += ", "
            trackList.append(i["track"]["name"] + " - " + nameString)

    # If playlist is smaller than NUM_SONGS use first artist of first track and search using seed
    if len(trackList) != NUM_SONGS:
        print("Playlist does not have enough songs")

        # Get first artist
        track_info = trackList[0]
        end_index = track_info.find(",")
        if end_index == -1:
            end_index = len(track_info)
        artist = track_info[track_info.find("-") + 2 : end_index]

        print("Searching Spotify with artist {}".format(artist))

        attempts = NUM_ATTEMPTS
        while attempts != 0:
            song_limit = NUM_SONGS - len(trackList)

            # Exit loop if we received NUM_SONGS in the trackList
            if song_limit == 0:
                break

            print("Attempts Left {}".format(attempts - 1))

            # Spotify API to find search results
            search = spotify.search(q='artist:' + artist, type='artist')
            items = search['artists']['items']
            if len(items) > 0:
                artist = items[0]
                results = spotify.recommendations(seed_artists=[artist['external_urls']['spotify']], limit=song_limit)

            for i in results["tracks"]:
                # If there's only one artist add "trackName - artist"
                if (i["artists"].__len__() == 1):
                    trackList.append(i["name"] + " - " + i["artists"][0]["name"])
                # Else add "trackName - artist1, artist2, etc"
                else:
                    nameString = ""
                    for index, b in enumerate(i["artists"]):
                        nameString += (b["name"])
                        if (i["artists"].__len__() - 1 != index):
                            nameString += ", "
                    trackList.append(i["name"] + " - " + nameString)

    return trackList

# Comments use Youtube API rather than web scraping
def searchYoutube(songName):
    songName += " Music Video"
    #api = youtube.API(client_id=APIs["youtube"]["client_id"],
              #client_secret=APIs["youtube"]["client_secret"],
              #api_key=APIs["youtube"]["api_key"])
    #video = api.get('search', q=songName, maxResults=1, type='video', order='relevance')
    video = YoutubeSearch(songName, max_results=1).to_dict()
    #return video["items"][0]["id"]["videoId"]
    return video[0]["id"]

@application.route('/get-tracks', methods=['POST', 'GET'])
def getTracks():
    tracks = []

    if flask.request.method == 'POST':
        # Get user input and seach using Spotify API
        data = flask.request.get_json()
        try:
            if data['seed'] == "Artist":
                artist = data['search']
                tracks = getTracksFromSeed(artist, "artist")
                if artist == "Beyonce":
                    tracks = ["Crazy In Love ft. JAY Z - Beyonce", "Super Bass - Nicki Minaj", "Shake It Off - Mariah Carey", "Say My Name - Destiny's Child", "Umbrella ft. JAY Z - Rihanna", "Work It - Missy Elliot", "Genie In A Bottle - Christina Aguilera", "Not Another Love Song - Ella Mai", "Distraction - Kehlani", "No One - Alicia Keys", "Issues/Hold On - Teyana Taylor", "Love On Top - Beyonce", "Toxic - Britney Spears", "Creep - TLC", "Can't Remember to Forget You ft. Rihanna - Shakira", "Crazy In Love ft. JAY Z - Beyonce", "Super Bass - Nicki Minaj", "Shake It Off - Mariah Carey", "Say My Name - Destiny's Child", "Umbrella ft. JAY-Z - Rihanna", "Work It - Missy Elliot", "Genie In A Bottle - Christina Aguilera", "Not Another Love Song - Ella Mai", "Distraction - Kehlani", "No One - Alicia Keys", "Issues/Hold On - Teyana Taylor", "Love On Top - Beyonce", "Toxic - Britney Spears", "Creep - TLC", "Can't Remember to Forget You ft. Rihanna - Shakira", "Crazy In Love ft. JAY Z - Beyonce", "Super Bass - Nicki Minaj", "Shake It Off - Mariah Carey", "Say My Name - Destiny's Child", "Umbrella ft. JAY-Z - Rihanna", "Work It - Missy Elliot", "Genie In A Bottle - Christina Aguilera", "Not Another Love Song - Ella Mai", "Distraction - Kehlani", "No One - Alicia Keys", "Issues/Hold On - Teyana Taylor", "Love On Top - Beyonce", "Toxic - Britney Spears", "Creep - TLC", "Can't Remember to Forget You ft. Rihanna - Shakira", "Crazy In Love ft. JAY Z - Beyonce", "Super Bass - Nicki Minaj", "Shake It Off - Mariah Carey", "Say My Name - Destiny's Child", "Umbrella ft. JAY-Z - Rihanna", "Work It - Missy Elliot", "Genie In A Bottle - Christina Aguilera", "Not Another Love Song - Ella Mai", "Distraction - Kehlani", "No One - Alicia Keys", "Issues/Hold On - Teyana Taylor", "Love On Top - Beyonce", "Toxic - Britney Spears", "Creep - TLC", "Can't Remember to Forget You ft. Rihanna - Shakira"]
            elif data['seed'] == "Genre":
                genre = data['search']
                # Map rap to hip-hop as rap is not a real genre on Spotify
                if genre == "rap":
                    genre = "hip-hop"
                tracks = getTracksFromSeed(genre, "genre")
            elif data['seed'] == "Playlist":
                playlistURL = data['search']
                tracks = getTracksFromPlaylist(playlistURL) 
        except:
            print("Error using Spotify API")
    
    print("Tracks Found: {}".format(tracks))

    return flask.make_response(flask.jsonify({"tracks": tracks}))

@application.route('/get-video-id', methods=['POST', 'GET'])
def getVideoID():
    video_id = ""

    # Get YouTube video ID of track
    if flask.request.method == 'POST':
        data = flask.request.get_json()
        video_id = searchYoutube(data['track'])
        print("Searching YouTube with track {}".format(data['track']))
        print("Video ID Found: {}".format(video_id))

    return flask.make_response(flask.jsonify({"video_id": video_id}))

@application.route('/powerhour')
def powerhour():
    return flask.render_template('powerhour.html')

@application.route('/', methods=['POST', 'GET'])
def index():
    # token = spotipy.util.prompt_for_user_token(APIs["spotify"]["username"],
            # "playlist-modify-private",
            # client_id=APIs["spotify"]["client_id"],
            # client_secret=APIs["spotify"]["client_secret"],
            # redirect_uri='http://localhost:8080/')
    # spotify_client = spotipy.Spotify(auth=token)
    return flask.render_template('web.html')

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=True)