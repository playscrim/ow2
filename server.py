from flask import Flask, request
from dotenv import dotenv_values

from prisma import Prisma, register

from services.user import UserService
from oauth.battlenet import BattleNetOAuth

app = Flask(__name__)
config = dotenv_values('.env')

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

@app.route('/user/<int:user_id>')
def get_user_by_id(user_id):
  return user_service.find_one(user_id)

@app.route('/user/register', methods=['POST'])
def register_user():
  """Endpoint to register user
  ---
  responses:
    200:
      description: User created successfully
  """
  request_data = request.get_json()

  user_id = request_data['user_id']
  allow_code = request_data['allow_code']

  access_token = oauth.get_access_token(allow_code)
  battletag = oauth.get_user_info(access_token)

  user_dto = {
    'battletag': battletag,
    'allow_code': allow_code,
    'user_id': user_id
  }

  return user_service.create_user(user_dto).model_dump_json()

if __name__ == '__main__':
  app.run('0.0.0.0', 8000, debug=True)
