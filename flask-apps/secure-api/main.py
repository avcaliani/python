import uuid
from flask import Flask, jsonify, g
from flask_httpauth import HTTPTokenAuth
from token_service import Token
__author__  = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'


app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')
# You can change scheme, but it will affect your request token

@app.route('/')
def home():
    return "Wellcome to PYToken (with token)<br>By @avcaliani"

@app.route('/api/token')
def get_auth_token():
    new_uuid = uuid.uuid4()
    return jsonify({ 
        'uuid': str(new_uuid),
        'token': Token.generate_auth_token(str(new_uuid)).decode('ascii')
    })

@app.route('/api/user')
@auth.login_required
def check_auth_token():
    return jsonify({'uuid': g.current_user})
    
@auth.verify_token
def verify_token(token):
    g.current_user = Token.verify_auth_token(token)
    return  g.current_user != None

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)