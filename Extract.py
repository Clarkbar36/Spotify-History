import spotipy
from spotipy.oauth2 import SpotifyOAuth
import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('spotify.ini')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config["Spotify"]["SPOTIFY_CLIENT_ID"],
                                               client_secret=config["Spotify"]["SPOTIFY_CLIENT_SECRET"],
                                               redirect_uri=config["Spotify"]["SPOTIFY_REDIRECT_URI"],
                                               scope="user-read-recently-played"))

past = sp.current_user_recently_played(10)

norm_tracks = pd.json_normalize(past, "items")

