import spotipy
from spotipy.oauth2 import SpotifyOAuth
import configparser


def connect_spotify():
    config = configparser.ConfigParser()
    config.read('spotify.ini')

    cache_handler = spotipy.cache_handler.CacheFileHandler()
    spconn = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config["Spotify"]["SPOTIFY_CLIENT_ID"],
                                                       client_secret=config["Spotify"]["SPOTIFY_CLIENT_SECRET"],
                                                       redirect_uri=config["Spotify"]["SPOTIFY_REDIRECT_URI"],
                                                       scope="user-read-recently-played",
                                                       cache_handler=cache_handler,
                                                       show_dialog=True))
    return spconn
