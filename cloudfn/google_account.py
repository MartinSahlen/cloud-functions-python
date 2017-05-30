import os
from google.oauth2 import credentials


def get_credentials():
    return credentials.Credentials(os.getenv('GOOGLE_OAUTH_TOKEN', ''))
