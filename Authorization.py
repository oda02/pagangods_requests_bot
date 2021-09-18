import base64
import time
from requests_oauthlib import *


def get_token_pair(username, password):
    client_id = r'pagangods-mobile'
    redirect_uri = r'pagangods://oauthredirect/signin-oidc'
    response = requests.post('https://my.inanomo.com/api/v1/authentication', json={"username": username, "password": password, "returnUrl":"/connect/authorize/callback?client_id=pagangods-mobile&redirect_uri=pagangods%3A%2F%2Foauthredirect%2Fsignin-oidc&response_type=code&scope=pagan-gods%20offline_access&code_challenge=fzAAX9yn-51tePGkburt6Yi_ia92mZ81jndwP56sBHw&code_challenge_method=S256&response_method=query"})
    # print(response)
    s = response.headers['set-cookie']
    s1 = s[s.find('_s'):]
    s2 = s1[:s1.find(';')+1]
    # print(s2)
    try:
        response = requests.get('https://my.inanomo.com/connect/authorize/callback?client_id=pagangods-mobile&redirect_uri=pagangods%3A%2F%2Foauthredirect%2Fsignin-oidc&response_type=code&scope=pagan-gods%20offline_access&code_challenge=fzAAX9yn-51tePGkburt6Yi_ia92mZ81jndwP56sBHw&code_challenge_method=S256&response_method=query', headers={'cookie':s})
    except Exception as err:
        code = str(err)[str(err).find('code=')+5:str(err).find('&')]
        # print(code)
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    response = oauth.fetch_token(
            'https://my.inanomo.com/connect/token',
            code=code,
            code_verifier='hDYUjKFSDuSQmNeJcaJuS8K9H1iKw0PJxnRR_4o_bVWhFFXaqZStisBk13NQb56fFiZ.7ujhsjs9hCZbDI19M6aFmGxFo',
    )

    return {
        "access_token": response.get('access_token'),
        "refresh_token": response.get('refresh_token'),
        "expires_time": time.time() + response.get('expires_in')
    }


def refresh_token(refresh_token):
    # print(refresh_token)
    CLIENT_ID = "pagangods-mobile"
    CLIENT_SECRET = "your-client-secret"
    REDIRECT_URI = "pagangods://oauthredirect/signin-oidc"
    base64_encoded_clientid_clientsecret = base64.b64encode(
        str.encode(f'{CLIENT_ID}:{CLIENT_SECRET}'))  # concatenate with : and encode in base64
    base64_encoded_clientid_clientsecret = base64_encoded_clientid_clientsecret.decode(
        'ascii')  # turn bytes object into ascii string

    url = "https://my.inanomo.com/connect/token"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': f'Basic {base64_encoded_clientid_clientsecret}'
    }

    data = {'grant_type': 'refresh_token',
            'redirect_uri': REDIRECT_URI,
            'refresh_token': refresh_token
            }

    r = requests.post(url, headers=headers, data=data)
    response = r.json()
    # print(r)

    kok = {
        "access_token": response.get('access_token'),
        "refresh_token": response.get('refresh_token'),
        "expires_time": time.time() + response.get('expires_in')
    }

    return kok



