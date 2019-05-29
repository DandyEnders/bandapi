from bandapi import auth

print("""
I can get access_token for you, but I need you to follow my instructions.
I will:
    1. Try to get authorization code by sending http request
        from your login session on your browser. 
        ( so open the link on browser, login, and open link again.
        it will redirect with different url. 
        Or just open it once only, if you are already logged in. )
    2. Try to get authorization profile from authorization code I got.
    3. Return access_token and refresh_token to you.

""")

auth_profile = auth.get_new_auth_profile()

access_token = auth_profile['access_token']
refresh_token = auth_profile['refresh_token']

print(f"""
vv access_token vv
{access_token}

vv refresh_token vv
{refresh_token}

or

export BANDAPI_ACCESS_TOKEN={access_token}
export BANDAPI_REFRESH_TOKEN={refresh_token}
""")
