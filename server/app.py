from flask import Flask, jsonify, request, make_response, g
from flask import Blueprint
import json
from v1.user.router import UserRouter
from v1.item.router import ItemRouter
from v1.auth import login as auth_login, verify_token as auth_verify_token
from db import Db
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I/L0ve/CIT-U'
app.config['CORS_HEADERS'] = ['Content-Type', 'authorization']

CORS(app)
CORS(app, resources={r"*": {"origins": [
    'http://127.0.0.1:8080',
    'http://localhost:8080',
]}},  supports_credentials=True)

app.register_blueprint(UserRouter.handler())
app.register_blueprint(ItemRouter.handler())

@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.json
    if 'username' in data and 'password' in data:
        token = auth_login(data['username'], data['password'])
        if token is not False:
            return jsonify({'token': token})
    return jsonify({'message': 'Invalid username or password'}), 403

@app.route('/api/v1/login')
def home():
    return jsonify({'message': 'hello world'})

@app.route('/api/v1/verify-token')
def verify_token():
    token = request.args.get('token')
    if not auth_verify_token(token):
        return jsonify({'message': 'Invalid token'}), 403
    return jsonify({'ok': 'Token is valid'})

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0',port=8081)
    # app.run(debug=True,host='0.0.0.0',port=8080)
