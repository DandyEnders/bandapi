"""
Utility function
"""

from requests import request

from bandapi import config
import json

def print_json(string, indent=4, sort_keys=False):
    """
    Neatly print string into json-like format.
    """
    obj = json.loads(string)
    string = json.dumps(obj, indent=indent, sort_keys=sort_keys)
    print(string)
