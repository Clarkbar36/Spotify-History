import sqlalchemy as sa
import configparser


def import_stg_tbl(streamT, albumT, trackT, artistT):
    config = configparser.ConfigParser()
    config.read('spotify.ini')

    connection_uri = sa.engine.url.URL.create(
        "mssql+pyodbc",
        username=config["SQL Server"]["sql_uid"],
        password=config["SQL Server"]["sql_pwd"],
        host=config["SQL Server"]["sql_host"],
        database=config["SQL Server"]["sql_db"],
        query={"driver": config["SQL Server"]["sql_odbc_driver"]})

    engine = sa.create_engine(connection_uri)

    streamT.to_sql('stg.spotifyStream', engine, if_exists='replace', index=False, dtype={'playedAt': sa.DateTime()})
    albumT.to_sql('stg.spotifyAlbums', engine, if_exists='replace', index=False)
    trackT.to_sql('stg.spotifyTracks', engine, if_exists='replace', index=False)
    artistT.to_sql('prd.spotifyArtist', engine, if_exists='replace', index=False)
    engine.dispose()
