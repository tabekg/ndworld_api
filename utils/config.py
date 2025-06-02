from utils.parser import Config

config = Config()

MODE = config.get('system', 'mode')
IS_DEBUG_MODE = MODE == 'dev'
DB_URL = config.get('system', 'db_url')
API_URL = config.get('system', 'api_url')
API_VERSION = config.get('system', 'api_version')
WEB_URL = config.get('system', 'web_url')
STORAGE_PATH = config.get('system', 'storage_path')
PORT = config.get('system', 'port')
SECRET_KEY = config.get('system', 'secret_key')
STORAGE_DIRECTORIES = []

ACCESS_TOKEN_EXPIRE_DAYS = 90

DEFAULT_LANGUAGE = 'tr'
