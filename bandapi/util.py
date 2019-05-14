from requests import request

from bandapi import config


def do_request(url, method='GET'):
    """
    Makes a request and returns the result.
    """
    res = request(method=method, url=url)
    return res


def make_url(base, kwargs={}):
    """
    base -- str
        The base url until argument.
    kwargs -- dict
        The key arguments dict to be placed in url

    base + kwargs
    -->
    "baseurl?key1=value1&key2=value2&...&keyN=valueN"
    """
    kwargs = {'access_token': config.ACCESS_TOKEN, **kwargs}
    params = []

    # [key=value, key=value, ... ]
    for key, value in kwargs.items():
        if value:
            params.append(f'{key}={value}')
    # 'key=value&key=value...'
    params_url = '&'.join(params)
    # 'base?key=value&key=value...'
    url = f'{base}?{params_url}'

    return url


def api_request(base, kwargs={}, method='GET'):
    """
    Does api request and gets the results back.
    """
    url = make_url(base, kwargs)
    res = do_request(url, method=method)
    return res
