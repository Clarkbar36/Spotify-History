import sqlalchemy as sa
import configparser
import os


def merge_stg_to_prd():
    config = configparser.ConfigParser()
    config.read('spotify.ini')

    connection_uri = sa.engine.url.URL.create("mssql+pyodbc",
                                              username=config["SQL Server"]["sql_uid"],
                                              password=config["SQL Server"]["sql_pwd"],
                                              host=config["SQL Server"]["sql_host"],
                                              database=config["SQL Server"]["sql_db"],
                                              query={"driver": config["SQL Server"]["sql_odbc_driver"]})

    engine = sa.create_engine(connection_uri)

    # assign directory
    directory = 'sql'

    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        file = open(f)
        escaped_sql = sa.text(file.read())
        engine.execute(escaped_sql)
    engine.dispose()
