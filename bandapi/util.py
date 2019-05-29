"""
Utility function
"""

from requests import request

from bandapi import config
import json
import os


def print_json(string, indent=4, sort_keys=False):
    """
    Neatly print string into json-like format.
    """
    obj = json.loads(string)
    string = json.dumps(obj, indent=indent, sort_keys=sort_keys)
    print(string)


def purge_env_var():
    del os.environ['BANDAPI_CLIENT_ID']
    del os.environ['BANDAPI_CLIENT_SECRET']
    del os.environ['BANDAPI_REDIRECT_URL']
    del os.environ['BANDAPI_ACCESS_TOKEN']
    del os.environ['BANDAPI_REFRESH_TOKEN']
