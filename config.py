import os
import re
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('MERCURY_BOT')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
AUTO_LIST_URL = os.getenv('AUTO_LIST_URL')
CHECK_DATES_JSON = os.getenv('CHECK_DATES_JSON')
AUTHORIZATION_URL = os.getenv('AUTHORIZATION_URL')

MAIN_HTML = None
AUTO_HTML = None

ACCESS = 0
AUTO_ACCESS = 0

LOG = ''
PASS = ''
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')

PLATE_PATTERN = re.compile(r'^[A-Z]\d{3}[A-Z]{2}\d{2,3}$')
