import urllib

import requests
from requests.auth import HTTPBasicAuth

class BattleNetOAuth:
  """Used to make requests to the Battle.net API
  """
  BASE_URL = 'https://us.battle.net/oauth'
  BASE_QUERY = {
    'redirect_uri': 'http://localhost:8000/callback',
    'scope': 'openid',
  }

  def __init__(self, client_id, secret) -> None:
    self.__client_id = client_id
    self.__secret = secret
    
  def _build_query(self, **kwargs):
    query = dict(kwargs, **self.BASE_QUERY)
    return urllib.parse.urlencode(query)

  def _build_url(self, endpoint, query = None):
    has_query = f'?{query}' if query else ''
    return f'{self.BASE_URL}/{endpoint}{has_query}'

  def get_authorization(self, user_id):
    authorization = {
      'client_id': self.__client_id,
      'state': user_id,
      'response_type': 'code'
    }

    query = self._build_query(**authorization)

    return self._build_url('authorize', query)
  
  def get_access_token(self, allow_code):
    access = {
      'grant_type': 'authorization_code',
      'code': allow_code
    }

    query = self._build_query(**access)
    url = self._build_url('token')
    
    response = requests.post(
      url, 
      params=query, 
      auth=HTTPBasicAuth(self.__client_id, self.__secret)
    )

    return response.json()['access_token']

  def get_user_info(self, access_token):
    headers = {
      'Authorization': f'Bearer {access_token}'
    }

    url = self._build_url('userinfo')
    response = requests.get(url, headers=headers)

    return response.json()['battletag']
