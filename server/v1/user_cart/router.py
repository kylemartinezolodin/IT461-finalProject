from flask import Blueprint
from v1.user_cart.controller import User_CartController
from v1.auth import jwt_token_required

class User_CartRouter():
    @staticmethod
    def handler():
        app = Blueprint('users_cart', __name__, url_prefix='/api/v1/users_cart')
        app.before_request(jwt_token_required)
        controller = User_CartController()
        app.add_url_rule('/', methods=['POST'], view_func=controller.post)
        app.add_url_rule('/', methods=['GET'], view_func=controller.get)
        app.add_url_rule('/', methods=['PUT'], view_func=controller.put)
        app.add_url_rule('/', methods=['DELETE'], view_func=controller.delete)
        app.add_url_rule('/<user_cart_id>', methods=['GET'], view_func=controller.get)
        app.add_url_rule('/<user_cart_id>', methods=['PUT'], view_func=controller.put)
        app.add_url_rule('/<user_cart_id>', methods=['DELETE'], view_func=controller.delete)
        return app