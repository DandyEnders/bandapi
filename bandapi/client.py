import unittest
import json

import requests

from bandapi import auth

import pandas as pd


class APIClient:
    """
    The band API client.

    If any optional argument is None, the arugment will not be
    part of url to request. (Ex. client.get_profile(get_profile=None))
    """

    def __init__(self,
                 access_token=None,
                 auth_code=None
                 ):
        """
        APIClient init.

        Parameter
            access_token
                if given, Client skips manual http request.

            auth_code
                if given, Client skips manual http request.
                if both access_token and auth_code are given, this raises ValueError.
        """
        if access_token and auth_code:
            raise ValueError(
                'You must give value to either access_token or auth_code or both None.')

        if not access_token:
            access_token = auth.get_access_token(auth_code)

        self.access_token = access_token

    def get(self, url, kwargs):
        params = {'access_token': self.access_token,
                  **kwargs}
        return requests.get(url, params=params)

    def post(self, url, kwargs):
        params = {'access_token': self.access_token,
                  **kwargs}
        return requests.post(url, data=params)

    def api_request(self, method, url, kwargs):
        """
        Does actual band API request.

        Parameter
            method: str
                method_dict keys (get, post, ...)

            url: str
            kwargs: dict

        Raise
            ValueError
                if method != any of method_dict keys
        """
        method_dict = {
            'get': self.get,
            'post': self.post,
        }

        # if invalid method, throws KeyError
        try:
            call_func = method_dict[method.lower()]
        except KeyError:
            methods = str(list(method_dict.keys()))
            raise ValueError(f'Method must be one of: {methods}')

        response = call_func(url, kwargs)
        content_str = response._content.decode('utf-8')
        content_dict = json.loads(content_str)

        reason = response.reason.lower()
        if reason == 'ok':
            # 0 means fail, 1 means success
            # TODO: error handler for result_code status
            #result_code = content_dict.get('result_code', 0)
            result_data = content_dict.get('result_data', {})

            return result_data
        else:
            if reason == 'unauthorized':
                raise ConnectionRefusedError(
                    f'Current access_token is unauthorized: {self.access_token}\n Try to get a new one.')

    def get_profile(self,
                    band_key: str = None,
                    ):
        """
        Gets user's profile information.

        Return
            pd.DataFrame
                if band_key:
                    columns: [name, profile_image_url, member_name, 
                              member_profile_image_url, member_joined_at, 
                              user_key, is_app_member, message_allowed]
                if not band_key:
                    columns: [name, profile_image_url, user_key, 
                              is_app_member, message_allowed]
        """
        kwargs = locals()  # function param=arg dict
        url = "https://openapi.band.us/v2/profile"
        result_data = self.api_request('get', url, kwargs)
        result_data = pd.DataFrame.from_records(result_data, index=[0])
        return result_data

    def get_bands(self,
                  ):
        """
        Gets list of bands the user is involved in.

        Return
            pd.DataFrame
                columns: [band_key, cover, member_count, name]
        """
        kwargs = locals()  # function param=arg dict
        url = "https://openapi.band.us/v2.1/bands"
        result_data = self.api_request('get', url, kwargs)
        result_data = pd.DataFrame.from_records(result_data['bands'])
        return result_data

    def get_posts(self,
                  band_key: str,
                  locale: str = 'ko_KR'
                  ):
        """
        Gets list of posts.

        Band API only allows 20 posts to be cralwed per request.
        "limit" parameter does not work.

        Return
            dictionary
        """
        kwargs = locals()  # function param=arg dict
        url = "https://openapi.band.us/v2/band/posts"
        result_data = self.api_request('get', url, kwargs)
        #result_data = pd.DataFrame.from_records(result_data['bands'])
        return result_data

    def get_specific_post(self,
                          band_key: str,
                          post_key: str,
                          ):
        # TODO:
        raise NotImplementedError

    def write_post(self,
                   band_key,
                   content,
                   do_push=''):
        """
        NOT TESTED

        Uploads a post.

        Warning
            Contents seems to work only with English words.
        """
        kwargs = locals()  # function param=arg dict
        kwargs['content'] = kwargs['content'].replace(
            ' ', '%20')  # all space = %20
        url = "https://openapi.band.us/v2.2/band/post/create"
        result_data = self.api_request('post', url, kwargs)
        return result_data

    def delete_post(self,
                    band_key: str,
                    post_key: str,
                    ):
        # TODO:
        raise NotImplementedError

    def get_comments(self,
                     band_key: str,
                     post_key: str,
                     sortby: str = '+created_at',
                     ):
        # TODO:
        raise NotImplementedError

    def write_comment(self,
                      band_key: str,
                      post_key: str,
                      body: str,
                      ):
        # TODO:
        raise NotImplementedError

    def delete_comment(self,
                       band_key: str,
                       post_key: str,
                       comment_key: str,  # post_key on api doc
                       ):
        # TODO:
        raise NotImplementedError

    def check_permission(self,
                         band_key: str,
                         permissions: str,  # posting, commenting, contents_deletion
                         ):
        # TODO:
        raise NotImplementedError

    def get_albums(self,
                   band_key: str,
                   ):
        # TODO:
        raise NotImplementedError

    def get_photos(self,
                   band_key: str,
                   photo_album_key: str = None,
                   ):
        # TODO:
        raise NotImplementedError


class APIClientTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_profile(self):
        self.client.get_profile()


if __name__ == '__main__':
    unittest.main()
