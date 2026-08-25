import os
from . import config


class ConnectDB(object):
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        # Supabase PostgreSQL
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # MySQL lokal sebagai cadangan
        SQLALCHEMY_DATABASE_URI = (
            "mysql+pymysql://"
            + str(config.DB_USER or "")
            + ":"
            + str(config.DB_PASS or "")
            + "@"
            + str(config.DB_HOST or "localhost")
            + "/"
            + str(config.DB_NAME or "")
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True