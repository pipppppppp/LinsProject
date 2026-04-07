from . import config

class ConnectDB(object):
    DATABASE = config.DB_NAME
    USERNAME = config.DB_USER
    PASSWORD = config.DB_DWB
    HOST = config.DB_HOST

    SQLALCHEMY_DATABASE_URL = '' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True