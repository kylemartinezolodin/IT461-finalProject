from flask import jsonify, request, current_app
import jwt
import datetime
from db import Db
import hashlib, hmac

def jwt_token_required():
    token = request.args.get('token')
    if not token:
        return jsonify({'message': 'Token is required'}), 403
    if not verify_token(token):
        return jsonify({'message': 'Token is invalid or expired'}), 403

def verify_token(token):
    try:
        decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')
    except:
        return False
    return decoded_token

def login(username, password):
    db = Db.get_instance()
    sql = "SELECT * FROM users WHERE password = %s AND username = %s"
    
    if username != "admin": # do not hash when logging in to admin, since its the only way to have a valid token and u could not hash password during initialization of that user
        password = hashlib.md5(password.encode()).hexdigest() # hash the password
        # hmac.new('key', 'msg').hexdigest() # use when above is inconsistent (di ko sure sa consistency sa private key) FROM:https://stackoverflow.com/questions/697134/how-to-set-the-crypto-key-for-pythons-md5-module
    
    user = db.fetchone(sql,(password, username))
    if user:
        payload = {
            'username': user["username"],
            'id': user["id"],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
    return False
