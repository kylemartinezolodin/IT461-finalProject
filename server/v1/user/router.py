from flask import Blueprint
from v1.user.controller import UserController
from v1.auth import jwt_token_required

class UserRouter():
    @staticmethod
    def handler():
        app = Blueprint('users', __name__, url_prefix='/v1/users')
        app.before_request(jwt_token_required)
        controller = UserController()
        app.add_url_rule('/', methods=['POST'], view_func=controller.post)
        app.add_url_rule('/', methods=['GET'], view_func=controller.get)
        app.add_url_rule('/', methods=['PUT'], view_func=controller.put)
        app.add_url_rule('/', methods=['DELETE'], view_func=controller.delete)

        app.add_url_rule('/<user_id>', methods=['GET'], view_func=controller.get)
        app.add_url_rule('/<user_id>', methods=['PUT'], view_func=controller.put)
        app.add_url_rule('/<user_id>', methods=['DELETE'], view_func=controller.delete)
        return app