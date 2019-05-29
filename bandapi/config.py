import base64
import os

# Make app from https://developers.band.us/develop/myapps/list
CLIENT_ID = os.environ['BANDAPI_CLIENT_ID']
CLIENT_SECRET = os.environ['BANDAPI_CLIENT_SECRET']
# this is from the web profile but
# I have no idea where this is used for.
# This does not work as access_token on actual api call.
_ACCESS_TOKEN = ""
CLIENT_REDIRECT_URL = os.environ['BANDAPI_REDIRECT_URL']

# Auth Secret Header (ASH) - Not defined in band doc ( I named it )
# Used when requesting access token
_ash = f"{CLIENT_ID}:{CLIENT_SECRET}"
_ash = bytes(_ash, "utf8")
_ash = base64.b64encode(_ash)
_ash = _ash.decode()
AUTH_SECRET_HEADER = _ash

ACCESS_TOKEN = os.environ.get('BANDAPI_ACCESS_TOKEN', "")
REFRESH_TOKEN = os.environ.get('BANDAPI_REFRESH_TOKEN', "")
