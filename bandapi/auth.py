from bandapi import config
from urllib.parse import urlparse

import requests
import json


def get_new_auth_code(client_id=config.CLIENT_ID,
                      client_redirect_url=config.CLIENT_REDIRECT_URL,
                      ):
    """
    Gets authorization code to use to get access_token.

    Parameter
        client_id: str
        client_redirect_url:str

    Description
        Gets autho_code from http request.
        Asks user to do the http request on browser because
        getting auth_code requires login session.

    Return
        auth_code: str
    """

    print("Open this link on your browser:")
    auth_url = f"https://auth.band.us/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={client_redirect_url}"
    print(f'{auth_url}')

    full_url = input("Paste redirected full url: \n")

    # https://auth.band.us/oauth2/{red_url}?code={auth_code}
    # ParseResult(scheme='https', netloc='auth.band.us', path='/oauth2/www.example.com', params='', query='code={auth_code}', fragment='')
    parsed_url = urlparse(full_url)

    # get query, split along =, get value -> auth_code
    # ['code', {auth_code}][-1] = {auth_code}
    auth_code = parsed_url.query.split('=')[-1]
    return auth_code


def _check_token_profile_error(token_profile):
    # error catch
    if 'error' in token_profile.keys():
        error_reason = token_profile['error'].lower()
        error_desc = token_profile['error_description']

        if error_reason == 'unauthorized':
            raise ValueError(f'''API authorization failed: {error_desc}
                            Possibly due to wrong client_secret.''')

        if error_reason == 'invalid_grant':
            raise ValueError(
                f'''API authorization failed: {error_desc}
                Possibly due to wrong auth_code or refresh_token.''')


def get_new_auth_profile(auth_code=None,
                         client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         ):
    """
    Gets band authorization profile dictionary.

    Parameter
        auth_code: str
            if not auth_code, get_new_auth_code will be called.

        client_id: str
        client_secret: str

    Description
        This method gets band auth profile by asking for
        auth_code(which requires login, that is why I deliberately
        made user to do http request on the browser),
        and by requesting access_token by specified http request.

    Return
        dict
            "access_token": {str},
            "token_type": {str},
            "refresh_token": {str},
            "expires_in": {int},
            "scope": {str},
            "user_key": {str}

    Sample
        {
            "access_token": "{token_str}",
            "token_type": "bearer",
            "refresh_token": "{refresh_token_str}",
            "expires_in": {time_int},
            "scope": "WRITE_POST READ_MY_PROFILE READ_POST DELETE_POST READ_ALBUM \
                        READ_PHOTO READ_BAND_PERMISSION READ_COMMENT \
                        READ_BAND_AND_USERS_LIST DELETE_COMMENT CREATE_COMMENT",
            "user_key": "{user_key_str}"
        }
    """
    if not auth_code:
        auth_code = get_new_auth_code()

    auth_secret_header = config.AUTH_SECRET_HEADER

    query = {
        "grant_type": "authorization_code",
        "code": auth_code,
    }
    url = "https://auth.band.us/oauth2/token"

    headers = {
        "Authorization": f"Basic {auth_secret_header}"
    }
    res = requests.get(url, params=query, headers=headers)

    message = res.text
    token_profile = json.loads(message)

    _check_token_profile_error(token_profile)

    return token_profile


def get_refreshed_auth_profile(refresh_token,
                               client_id=config.CLIENT_ID,
                               client_secret=config.CLIENT_SECRET,
                               ):
    """
    Gets band authorization profile dictionary.

    Parameter
        refresh_token: str
            refresh_token you get from auth_profile['refresh_token'].

        client_id: str
        client_secret: str

    Description
        Requests new auth_profile using refresh_token aquired.

    Return
        dict
            "access_token": {str},
            "token_type": {str},
            "refresh_token": {str},
            "expires_in": {int},
            "scope": {str},
            "user_key": {str}

    Sample
        {
            "access_token": "{token_str}",
            "token_type": "bearer",
            "refresh_token": "{refresh_token_str}",
            "expires_in": {time_int},
            "scope": "WRITE_POST READ_MY_PROFILE READ_POST DELETE_POST READ_ALBUM \
                        READ_PHOTO READ_BAND_PERMISSION READ_COMMENT \
                        READ_BAND_AND_USERS_LIST DELETE_COMMENT CREATE_COMMENT",
            "user_key": "{user_key_str}"
        }
    """
    auth_secret_header = config.AUTH_SECRET_HEADER

    query = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    url = "https://auth.band.us/oauth2/token"

    headers = {
        "Authorization": f"Basic {auth_secret_header}"
    }
    res = requests.get(url, params=query, headers=headers)

    message = res.text
    token_profile = json.loads(message)

    _check_token_profile_error(token_profile)

    return token_profile


def get_access_token(refreshed=False,
                     client_id=config.CLIENT_ID,
                     client_secret=config.CLIENT_SECRET,
                     ):
    """
    Gets access_token.

    Description
        TODO:

    Return
        dict
            "access_token": {str},
            "token_type": {str},
            "refresh_token": {str},
            "expires_in": {int},
            "scope": {str},
            "user_key": {str}

    """

    if refreshed:
        if config.REFRESH_TOKEN:
            auth_profile = get_refreshed_auth_profile(config.REFRESH_TOKEN,
                                                      client_id=client_id,
                                                      client_secret=client_secret,
                                                      )
            print(auth_profile)
            access_token = auth_profile['access_token']
        else:
            raise KeyError('BANDAPI_REFRESH_TOKEN')

    elif not refreshed:
        if config.ACCESS_TOKEN:
            access_token = config.ACCESS_TOKEN
        else:
            raise KeyError('BANDAPI_ACCESS_TOKEN')

    return access_token


if __name__ == "__main__":
    profile = get_new_auth_profile()
