from flask import request, make_response, jsonify
from v1.basecontroller import BaseController
from v1.user_cart.model import User_CartModel

class User_CartController(BaseController):
    _instance = None

    def __init__(self) -> None:
        self._instance = User_CartModel()

    def post(self):
        print(request.json)
        resp = self._instance.create(request.json)
        if resp == False:
            return make_response(jsonify({
                "error": "Failed to add. There are users_cart in your request that are invalid."
            }), 400)
        return jsonify(resp)

    def check(self, user_cart_id, filters=None):
        if filters is not None:
            filters['id'] = user_cart_id
        else:
            filters = {"id": user_cart_id}
        user_cart = self._instance.read(filters)
        if user_cart is None:
            return make_response(jsonify({"error": "Item id not found."}), 404)
        return user_cart

    def get(self, user_cart_id=None):
        filters = {}
        if 'fields' in request.args:
            filters['fields'] = request.args['fields'].split(',')
        if user_cart_id is not None:
            user_cart = self.check(user_cart_id, filters)
            if not isinstance(user_cart, dict):
                return {"data":user_cart}
            return jsonify(user_cart)
        filters['offset'] = int(request.args['offset']) if 'offset' in request.args else 0
        filters['limit'] = int(request.args['limit']) if 'limit' in request.args else 5
        users_cart = self._instance.read(filters)
        total = self._instance.read(filters, True)
        return jsonify({
            'metadata': {
                'total': total,
                'links': self.build_links(total, filters['offset'], filters['limit'])
            },
            'data': users_cart
        })

    def put(self, user_cart_id=None):
        if user_cart_id is not None:
            user_cart = self.check(user_cart_id)
            if not isinstance(user_cart, dict):
                return user_cart
            user_cart_data = request.json
            user_cart_data['id'] = user_cart_id
            resp = self._instance.update(user_cart_data)
            if resp == False:
                return make_response(jsonify({
                    "error": "Failed to update. There are users_cart in your request that are invalid."
                }), 400)
            return jsonify(resp)
        return jsonify(self._instance.update(request.json))

    def delete(self, user_cart_id=None):
        if user_cart_id is not None:
            user_cart = self.check(user_cart_id)
            if not isinstance(user_cart, dict):
                return user_cart
            return jsonify(self._instance.delete(user_cart_id))
        return jsonify(self._instance.delete(request.json))