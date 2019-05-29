
# bandapi

A wrapper for Naver Band API.

# Set up

1. Make app from <https://developers.band.us/develop/myapps/list>
1. Get client_id, client_secret, redirect_url and add env
   variables:

    ```bash
    export BANDAPI_CLIENT_ID=
    export BANDAPI_CLIENT_SECRET=
    export BANDAPI_REDIRECT_URL=
    ```

    WARNING: Make sure those env variables are correct.
    I could not find a good way to test if input values are
    correct.

1. After that, you can either get access_token
   and refresh_token by yourself or execute **get_token.py**
   and follow its instructions to get tokens.

   Once you aquired those tokens, add these env variables:

    ```bash
    export BANDAPI_ACCESS_TOKEN=
    export BANDAPI_REFRESH_TOKEN=
    ```

1. Now you are ready to use bandapi/band.py as a wrapper.