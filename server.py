from flask import Flask, request
from dotenv import dotenv_values

from prisma import Prisma, register

from services.user import UserService
from oauth.battlenet import BattleNetOAuth

app = Flask(__name__)
config = dotenv_values('.env')

"""Dependency Injection
"""
oauth = BattleNetOAuth(
  config['CLIENT_ID'], 
  config['CLIENT_SECRET']
)

prisma = Prisma()
prisma.connect()

register(prisma)

user_service = UserService()
 
@app.route('/')
def index():
  return oauth.get_authorization(432354788219420683)

@app.route('/callback')
def callback():
  allow_code = request.args.get('code')
  user_id = request.args.get('state')

  access_token = oauth.get_access_token(allow_code)
  battletag = oauth.get_user_info(access_token)

  dto = {
    'battletag': battletag,
    'allow_code': allow_code,
    'user_id': int(user_id)
  }

  return user_service.create_user(dto).model_dump_json()

if __name__ == '__main__':
  app.run('0.0.0.0', 8000, debug=True)
