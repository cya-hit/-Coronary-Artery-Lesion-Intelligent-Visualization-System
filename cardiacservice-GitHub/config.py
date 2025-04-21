'''线上环境'''
class Config():
    """config"""
    SECRET_KEY = ""
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False

    REDIS_HOST = ""
    REDIS_PORT =
    REDIS_DB =
    MSG_QUEUE = ""
    QUEUE_MAX =

    USER_TOKEN_KEY = ""
    TOKEN_EXPIRE =

    DEBUG = False

    DICOMZIP_DIR = ""
    DICOM_DIR = ""
    UPLOADSTL_DIR = ""
    IMG_DIR = ""
    IMG_PREFIX = ""
    NIIDATA_DIR = ""
    AISTL_DIR = ""
