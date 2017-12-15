from requests_oauthlib import OAuth2Session

import webbrowser
import json
# from datetime import datetime

from secret_data import *



## CACHING SETUP
#--------------------------------------------------
# Caching constants
#--------------------------------------------------

# DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG = True
CACHE_FNAME = "cache_contents.json"
CREDS_CACHE_FILE = "creds.json"

#--------------------------------------------------
# Load cache files: data and credentials
#--------------------------------------------------
# Load data cache
try:
    with open(CACHE_FNAME, 'r') as cache_file:
        cache_json = cache_file.read()
        CACHE_DICTION = json.loads(cache_json)
except:
    CACHE_DICTION = {}

# Load creds cache
try:
    with open(CREDS_CACHE_FILE,'r') as creds_file:
        cache_creds = creds_file.read()
        CREDS_DICTION = json.loads(cache_creds)
except:
    CREDS_DICTION = {}

#---------------------------------------------
# Cache functions
#---------------------------------------------
def get_from_cache(identifier, dictionary):
    """If unique identifier exists in specified cache dictionary, return the data associated with it from the request, else return None"""
    identifier = identifier.upper() # Assuming none will differ with case sensitivity here
    if identifier in dictionary:
        data = dictionary[identifier]['values']
    else:
        data = None
    return data


def set_in_data_cache(identifier, data):
    """Add identifier and its associated values (literal data) to the data cache dictionary, and save the whole dictionary to a file as json"""
    identifier = identifier.upper()
    CACHE_DICTION[identifier] = {
        'values': data
        # 'timestamp': datetime.now().strftime(DATETIME_FORMAT)
    }

    with open(CACHE_FNAME, 'w') as cache_file:
        cache_json = json.dumps(CACHE_DICTION)
        cache_file.write(cache_json)

def set_in_creds_cache(identifier, data):
    """Add identifier and its associated values (literal data) to the credentials cache dictionary, and save the whole dictionary to a file as json"""
    identifier = identifier.upper() # make unique
    CREDS_DICTION[identifier] = {
        'values': data
        # 'timestamp': datetime.now().strftime(DATETIME_FORMAT)
    }

    with open(CREDS_CACHE_FILE, 'w') as cache_file:
        cache_json = json.dumps(CREDS_DICTION)
        cache_file.write(cache_json)


#####
## Oauth2 authentication setup, functions to get and process data, a class definition... etc.
### Private data in a hidden secret_data.py file

# for Instagram OAuth (Ins uses OAuth2)
# https://www.instagram.com/developer/
# https://www.instagram.com/developer/authentication/

# Instagram Sandbox Permissions:
# Apps in sandbox are restricted to 10 users
# Data is restricted to 20 most recent media from each of those users
# Reduced API rate limits

ins_session = False
cached_user_list = []

APP_ID = client_key
APP_SECRET = client_secret
AUTHORIZATION_BASE_URL = 'https://api.instagram.com/oauth/authorize'
TOKEN_URL = 'https://api.instagram.com/oauth/access_token'
REDIRECT_URI = 'https://www.programsinformationpeople.org/runestone/oauth'
scope = ['basic']


def make_ins_request(username, url, params=None):
    # we use 'global' to tell python that we will be modifying this global variable
    global ins_session
    global cached_user_list
    
    if username not in cached_user_list:
        start_ins_session(username)
        cached_user_list.append(username)

    params['access_token'] = get_from_cache(username, CREDS_DICTION)['access_token']

    return ins_session.get(url, params=params)

def start_ins_session(username):

    global ins_session

    # 0 - get token from cache
    try:
        # token = get_saved_token()
        token = get_from_cache(username, CREDS_DICTION)
    except FileNotFoundError:
        token = None

    if token:
        ins_session = OAuth2Session(APP_ID, token=token, scope=scope)

    else:
        # 1 - session
        ins_session = OAuth2Session(APP_ID, redirect_uri=REDIRECT_URI, scope=scope)

        # 2 - authorization
        authorization_url, state = ins_session.authorization_url(AUTHORIZATION_BASE_URL)
        print('Opening browser to {} for authorization'.format(authorization_url))
        webbrowser.open(authorization_url)

        # 3 - token
        redirect_response = input('Paste the full redirect URL here: ')
        token = ins_session.fetch_token(TOKEN_URL, client_secret=APP_SECRET,
            authorization_response=redirect_response.strip())

        # 4 - save_token
        if DEBUG:
            print ("access token: " )
            print (token)
        set_in_creds_cache(username,token)


def get_data_from_api(identifier, url, params):
    """Check in cache, if not found, load data, save in cache and then return that data"""
    data = get_from_cache(identifier,CACHE_DICTION)
    if data:
        if DEBUG:
            print("Loading from data cache: {}... data".format(identifier))
    else:
        if DEBUG:
            print("Fetching new data from {}".format(identifier))
        response = make_ins_request(identifier,url, params)
        if DEBUG:
            print(response.text)
        data = response.json()
        set_in_data_cache(identifier, data)

    return data
