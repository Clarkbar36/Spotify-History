from scripts.spotify_connect import connect_spotify
from scripts.pull_recent import pull_recently_played
from scripts.pull_track import pull_track_info
from scripts.pull_features import pull_features
from scripts.pull_artist import pull_artist_info
from scripts.combine_data import combine_data
from scripts.save_to_csv import save_csv

sp = connect_spotify()
basic_info = pull_recently_played(sp)
artist_track_info = pull_track_info(sp, basic_info)
track_features = pull_features(sp, basic_info)
artist_info = pull_artist_info(sp, artist_track_info)
most_recent_tracks = combine_data(basic_info, artist_track_info, track_features, artist_info)
save_csv(most_recent_tracks)




