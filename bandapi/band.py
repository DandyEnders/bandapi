import json

from bandapi.util import api_request


def get_profile(band_key=""):
    """
    Gets user's profile information.
    """
    kwargs = locals()  # function param=arg dict
    base = "https://openapi.band.us/v2/profile"
    return api_request(base, kwargs)


def get_bands():
    """
    Gets list of bands the user is involved in.
    """
    kwargs = locals()  # function param=arg dict
    base = "https://openapi.band.us/v2.1/bands"
    return api_request(base, kwargs)


def upload_post(band_key, content, do_push=''):
    """
    Uploads a post.

    Warning
        Contents seems to work only with English.
    """
    kwargs = locals()  # function param=arg dict
    kwargs['content'] = kwargs['content'].replace(' ', '%20')  # all space = %20
    base = "https://openapi.band.us/v2.2/band/post/create"
    return api_request(base, kwargs, method='POST')


def print_json(string, indent=4, sort_keys=False):
    """
    Neatly print string into json-like format.
    """
    obj = json.loads(string)
    string = json.dumps(obj, indent=indent, sort_keys=sort_keys)
    print(string)
