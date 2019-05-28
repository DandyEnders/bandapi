from bandapi import config
from urllib.parse import urlparse

import requests
import json
import base64


def get_auth_code(client_id=config.CLIENT_ID,
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

    print("Do http request using the following link:")
    auth_url = f"https://auth.band.us/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={client_redirect_url}"
    print(f'{auth_url}')

    full_url = input("Paste returned url: ")

    # https://auth.band.us/oauth2/{red_url}?code={auth_code}
    # ParseResult(scheme='https', netloc='auth.band.us', path='/oauth2/www.example.com', params='', query='code={auth_code}', fragment='')
    parsed_url = urlparse(full_url)
    # get query, split along =, get value -> auth_code
    # ['code', {auth_code}][-1] = {auth_code}
    auth_code = parsed_url.query.split('=')[-1]
    return auth_code


def get_auth_profile(auth_code=None,
                     client_id=config.CLIENT_ID,
                     client_secret=config.CLIENT_SECRET,
                     ):
    """
    Gets band authorization profile dictionary.

    Parameter
        auth_code: str
            if not auth_code, get_auth_code will be called.

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
        auth_code = get_auth_code()

    base64_param = f"{client_id}:{client_secret}"
    base64_param = bytes(base64_param, "utf8")
    base64_param = base64.b64encode(base64_param)
    base64_param = base64_param.decode()

    query = {
        "grant_type": "authorization_code",
        "code": auth_code,
    }
    url = "https://auth.band.us/oauth2/token"

    headers = {
        "Authorization": f"Basic {base64_param}"
    }
    res = requests.get(url, params=query, headers=headers)

    message = res.text
    token_profile = json.loads(message)

    # error catch
    if 'error' in token_profile.keys():
        error_reason = token_profile['error'].lower()
        error_desc = token_profile['error_description']
        
        if error_reason == 'unauthorized':
            raise ValueError(f'''API authorization failed: {error_desc}
                            Possibly due to wrong client_secret:{client_secret}''')

        if error_reason == 'invalid_grant':
            raise ValueError(
                f'''API authorization failed: {error_desc}
                Possibly due to wrong auth_code{auth_code}.''')

    return token_profile


def get_access_token(auth_code=None,
                     client_id=config.CLIENT_ID,
                     client_secret=config.CLIENT_SECRET,
                     ):
    """
    Gets access_token.

    Description
        This method encapsulates process of 
        getting access_token.
        View get_auth_profile for details.
    
    Return
        dict
            "access_token": {str},
            "token_type": {str},
            "refresh_token": {str},
            "expires_in": {int},
            "scope": {str},
            "user_key": {str}

    """
    profile = get_auth_profile(auth_code=auth_code,
                               client_id=client_id,
                               client_secret=client_secret)['access_token']
    return profile


if __name__ == "__main__":
    profile = get_auth_profile()
