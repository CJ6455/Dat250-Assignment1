import os

# contains application-wide configuration, and is loaded in __init__.py

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret' # TODO: Use this with wtforms
    RECAPTCHA_PUBLIC_KEY = '6LfxdRwiAAAAAPTyzwxSYuSXxpd2WWiyvHMEwQ6o'
    RECAPTCHA_PRIVATE_KEY ='6LfxdRwiAAAAAM-lE1ByKFukq71GqmlAE_Geluav'
    #SECURITY_PASSWORD_COMPLEXITY_CHECKER='zxcvbn'
    DATABASE = 'database.db'
    UPLOAD_PATH = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {'png','jpg','gif'} # Might use this at some point, probably don't want people to upload any file type
    MAX_CONTENT_LENGTH = 4*1024 * 1024