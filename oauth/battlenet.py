import urllib

import requests
from requests.auth import HTTPBasicAuth

class BattleNetOAuth:
  """Used to make requests to the Battle.net API
  """
  BASE_URL = 'https://us.battle.net/oauth'

  def __init__(self) -> None:
    self.query = {
      'redirect_uri': 'http://localhost:8000/callback',
      'scope': 'openid',
    }

  def get_authorization(self, user_id):
    authorization = {
      'client_id': 'f17e58b5a41e4688a74e5d0b10f3312f',
      'state': user_id,
      'response_type': 'code'
    }

    params = dict(authorization, **self.query)

    return f'{self.BASE_URL}/authorize?{urllib.parse.urlencode(params)}'
  
  def get_access_token(self, allow_code):
    access = {
      'grant_type': 'authorization_code',
      'code': allow_code
    }

    client_id = 'f17e58b5a41e4688a74e5d0b10f3312f'
    secret = 'P4cYNDzr8KW5O4rHG2r4VYZWHeXtz1Y1'

    params = dict(access, **self.query)
    url = f'{self.BASE_URL}/token'
    
    response = requests.post(url, params=params, auth=HTTPBasicAuth(client_id, secret))

    return response.json()['access_token']

  def get_user_info(self, access_token):
    headers = {
      'Authorization': f'Bearer {access_token}'
    }

    return requests.get(f'{self.BASE_URL}/userinfo', headers=headers).content
