from flask import Flask, request
from oauth.battlenet import BattleNetOAuth

app = Flask(__name__)
oauth = BattleNetOAuth()

@app.route('/')
def index():
  return oauth.get_authorization(432354788219420683)

@app.route('/callback')
def callback():
  allow_code = request.args.get('code')
  access_token = oauth.get_access_token(allow_code)

  return oauth.get_user_info(access_token)

if __name__ == '__main__':
  app.run('0.0.0.0', 8000, debug=True)
