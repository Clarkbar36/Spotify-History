from scripts.spotify_connect import connect_spotify
from scripts.pull_recent import pull_recently_played
from scripts.pull_features import pull_features
from scripts.pull_artist import pull_artist_info
from scripts.import_stg import import_stg_tbl
from scripts.merge_with_prd import merge_stg_to_prd
from scripts.save_to_s3 import upload_csv_to_s3

sp = connect_spotify()
basic_info, streamTable, albumTable = pull_recently_played(sp)
trackTable = pull_features(sp, basic_info)
artistTable = pull_artist_info(sp, basic_info)
import_stg_tbl(streamTable, albumTable, trackTable, artistTable)
merge_stg_to_prd()
upload_csv_to_s3(streamTable, albumTable, trackTable, artistTable)

##TODO figure out airflow




