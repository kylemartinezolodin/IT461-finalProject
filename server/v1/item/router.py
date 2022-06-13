from flask import Blueprint
from v1.item.controller import ItemController
from v1.auth import jwt_token_required

class ItemRouter():
    @staticmethod
    def handler():
        app = Blueprint('items', __name__, url_prefix='/api/v1/items')
        app.before_request(jwt_token_required)
        controller = ItemController()
        app.add_url_rule('/', methods=['POST'], view_func=controller.post)
        app.add_url_rule('/', methods=['GET'], view_func=controller.get)
        app.add_url_rule('/', methods=['PUT'], view_func=controller.put)
        app.add_url_rule('/', methods=['DELETE'], view_func=controller.delete)
        app.add_url_rule('/<item_id>', methods=['GET'], view_func=controller.get)
        app.add_url_rule('/<item_id>', methods=['PUT'], view_func=controller.put)
        app.add_url_rule('/<item_id>', methods=['DELETE'], view_func=controller.delete)
        return app